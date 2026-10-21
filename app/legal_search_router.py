"""Drop-in FastAPI router for the existing page-based Legal Intelligence FAISS index.

Place at <project_root>/app/legal_search_router.py and in app/main.py add:
    from app.legal_search_router import router as legal_search_router
    app.include_router(legal_search_router)

Does not edit existing modules. All source text is UNVERIFIED.
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'legal_law_collector' / 'processed'
INDEX_DIR = DATA / 'rag_index'
CHUNKS = DATA / 'rag_chunks.jsonl'

router = APIRouter(prefix='/api/legal', tags=['Legal RAG'])

class LegalSearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=2000)
    domain: Literal['rental', 'employment', 'divorce', 'property'] | None = None
    top_k: int = Field(default=5, ge=1, le=20)

@lru_cache(maxsize=1)
def load_retriever():
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError('Install dependencies: pip install sentence-transformers faiss-cpu numpy') from exc

    meta_file = INDEX_DIR / 'metadata.json'
    index_file = INDEX_DIR / 'legal_pages.faiss'
    for path in (meta_file, index_file, CHUNKS):
        if not path.is_file():
            raise RuntimeError(f'Missing {path}. Build index in legal_law_collector with: python build_legal_rag.py --index')

    metadata = json.loads(meta_file.read_text(encoding='utf-8'))
    digest = hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if digest != metadata.get('chunks_sha256'):
        raise RuntimeError('Chunks differ from FAISS index. Rebuild using python build_legal_rag.py --index')
    with CHUNKS.open(encoding='utf-8') as stream:
        chunks = [json.loads(line) for line in stream if line.strip()]
    index = faiss.read_index(str(index_file))
    if index.ntotal != len(chunks):
        raise RuntimeError('FAISS index and chunk count mismatch. Rebuild index.')
    model = SentenceTransformer(metadata['model'])
    return np, index, model, chunks

@router.get('/health')
def health():
    return {'status': 'ready' if (INDEX_DIR / 'legal_pages.faiss').is_file() else 'index_missing',
            'index_path': str(INDEX_DIR / 'legal_pages.faiss'),
            'verification_status': 'unverified'}

@router.post('/search')
def legal_search(request: LegalSearchRequest):
    try:
        np, index, model, chunks = load_retriever()
        # Search the full small corpus so a domain filter cannot miss relevant
        # results because other domains dominated the top few global hits.
        vector = np.asarray(model.encode([request.query], normalize_embeddings=True), dtype='float32')
        scores, indices = index.search(vector, index.ntotal if request.domain else min(index.ntotal, request.top_k))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            chunk = chunks[int(idx)]
            if request.domain and chunk.get('domain') != request.domain:
                continue
            results.append({
                'chunk_id': chunk['chunk_id'],
                'document_id': chunk['document_id'],
                'law_id': chunk.get('law_id'),
                'domain': chunk.get('domain'),
                'page': chunk.get('page'),
                'similarity': round(float(score), 4),
                'text': chunk['text'],
                'source_url': chunk.get('source_page_url'),
                'source_sha256': chunk.get('source_sha256'),
                'citation_granularity': 'document_page',
                'verification_status': 'unverified',
                'legal_status': chunk.get('legal_status', 'unknown'),
            })
            if len(results) >= request.top_k:
                break
        return {'query': request.query, 'domain': request.domain, 'count': len(results),
                'results': results, 'notice': 'Experimental retrieval only. Verify current law and PDF pages before legal citation.'}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
