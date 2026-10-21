"""Build provenance-preserving experimental legal RAG from processed/pages.jsonl.

Run:
    python build_legal_rag.py
    python build_legal_rag.py --index
    python build_legal_rag.py --search "notice period for tenant"

Optional indexing dependencies:
    pip install sentence-transformers faiss-cpu numpy

IMPORTANT: Source versions and legal currency are unverified. This tool does NOT
certify legal validity, section numbering, or the current state of the law.
"""
import argparse, collections, hashlib, json, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / 'processed'
CHUNKS = OUT / 'rag_chunks.jsonl'
INDEX_DIR = OUT / 'rag_index'
MODEL = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'


def chunk_text(text, size=1100, overlap=180):
    """Character-based chunks, always progressing, preferentially splitting on whitespace."""
    text = re.sub(r'\r\n?', '\n', text or '').strip()
    pos = 0
    while pos < len(text):
        stop = min(pos + size, len(text))
        if stop < len(text):
            split = max(text.rfind('\n', pos + size // 2, stop), text.rfind(' ', pos + size // 2, stop))
            if split > pos + size // 2:
                stop = split + 1
        content = text[pos:stop].strip()
        if content:
            yield pos, stop, content
        if stop >= len(text):
            break
        pos = max(pos + 1, stop - overlap)


def build_chunks(size=1100, overlap=180):
    if not 0 <= overlap < size // 2:
        raise ValueError('overlap must be >= 0 and less than half chunk size')
    source = OUT / 'pages.jsonl'
    if not source.exists():
        raise FileNotFoundError(f'Missing {source}')
    OUT.mkdir(exist_ok=True)
    count = 0
    docs = collections.Counter()
    with source.open(encoding='utf-8-sig') as inp, CHUNKS.open('w', encoding='utf-8') as dest:
        for lineno, line in enumerate(inp, 1):
            if not line.strip():
                continue
            try:
                page = json.loads(line)
                doc = str(page['document_id'])
                pageno = int(page['page'])
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(f'Invalid record on line {lineno}: {exc}') from exc
            for ordinal, (start, end, content) in enumerate(chunk_text(page.get('text', ''), size, overlap), 1):
                chunk_id = f'{doc}:p{pageno}:c{ordinal}'
                rec = {
                    'chunk_id': chunk_id, 'document_id': doc,
                    'law_id': page.get('law_id'), 'domain': page.get('domain'),
                    'jurisdiction': page.get('jurisdiction'), 'page': pageno,
                    'chunk_in_page': ordinal, 'start_char': start, 'end_char': end,
                    'text': content, 'source_page_url': page.get('source_page_url'),
                    'source_sha256': page.get('sha256'),
                    'legal_status': page.get('legal_status', 'unknown'),
                    'verification_status': 'unverified',
                    'section_number': None, 'citation_granularity': 'document_page',
                    'text_sha256': hashlib.sha256(content.encode('utf-8')).hexdigest(),
                }
                dest.write(json.dumps(rec, ensure_ascii=False) + '\n')
                count += 1
                docs[doc] += 1
    print(f'Created {CHUNKS} | {count} chunks | {len(docs)} documents')
    for doc, n in sorted(docs.items()):
        print(f'  {doc}: {n} chunks')
    return count


def load_chunks():
    if not CHUNKS.exists():
        build_chunks()
    with CHUNKS.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def dependencies():
    try:
        import numpy as np
        import faiss
        from sentence_transformers import SentenceTransformer
        return np, faiss, SentenceTransformer
    except ImportError as exc:
        raise SystemExit('Missing optional package. Install with: pip install sentence-transformers faiss-cpu numpy\n' + str(exc))


def index_chunks(batch_size=32):
    np, faiss, SentenceTransformer = dependencies()
    chunks = load_chunks()
    if not chunks:
        raise SystemExit('No chunks found; check processed/pages.jsonl')
    print('Loading embedding model (first run may download model files)...')
    model = SentenceTransformer(MODEL)
    INDEX_DIR.mkdir(exist_ok=True)
    index = None
    for start in range(0, len(chunks), batch_size):
        texts = [r['text'] for r in chunks[start:start + batch_size]]
        vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
        vectors = np.asarray(vectors, dtype='float32')
        if index is None:
            index = faiss.IndexFlatIP(vectors.shape[1])
        index.add(vectors)
        print(f'Embedded {min(start + batch_size, len(chunks))}/{len(chunks)}', end='\r', flush=True)
    faiss.write_index(index, str(INDEX_DIR / 'legal_pages.faiss'))
    (INDEX_DIR / 'metadata.json').write_text(json.dumps({
        'model': MODEL, 'chunk_count': len(chunks), 'chunks_sha256': hashlib.sha256(CHUNKS.read_bytes()).hexdigest(),
        'verification_status': 'unverified', 'citation_granularity': 'document_page'
    }, indent=2), encoding='utf-8')
    print(f'\nSaved {INDEX_DIR / "legal_pages.faiss"} ({index.ntotal} vectors)')


def search(query, k=5):
    np, faiss, SentenceTransformer = dependencies()
    meta_path = INDEX_DIR / 'metadata.json'
    idx_path = INDEX_DIR / 'legal_pages.faiss'
    if not meta_path.exists() or not idx_path.exists():
        raise SystemExit('Index not found. Run: python build_legal_rag.py --index')
    metadata = json.loads(meta_path.read_text(encoding='utf-8'))
    if hashlib.sha256(CHUNKS.read_bytes()).hexdigest() != metadata['chunks_sha256']:
        raise SystemExit('Chunks changed since indexing. Run: python build_legal_rag.py --index')
    chunks = load_chunks()
    index = faiss.read_index(str(idx_path))
    if index.ntotal != len(chunks):
        raise SystemExit('Index/chunk count mismatch. Rebuild with --index')
    model = SentenceTransformer(metadata['model'])
    vector = np.asarray(model.encode([query], normalize_embeddings=True), dtype='float32')
    scores, ids = index.search(vector, min(k, index.ntotal))
    for rank, (score, i) in enumerate(zip(scores[0], ids[0]), 1):
        if i < 0:
            continue
        c = chunks[int(i)]
        print(f'\n[{rank}] similarity={float(score):.3f} | {c["document_id"]} | PDF page {c["page"]} | {c["chunk_id"]}')
        print(f'Source: {c.get("source_page_url") or "Not recorded"}')
        print('UNVERIFIED SOURCE — verify official current text and page before citing.')
        print(c['text'][:650].replace('\n', ' '))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--index', action='store_true', help='Build FAISS embeddings/index')
    p.add_argument('--search', metavar='QUERY', help='Search indexed chunks')
    p.add_argument('--size', type=int, default=1100)
    p.add_argument('--overlap', type=int, default=180)
    p.add_argument('--top-k', type=int, default=5)
    args = p.parse_args()
    if args.search:
        search(args.search, args.top_k)
    elif args.index:
        build_chunks(args.size, args.overlap)
        index_chunks()
    else:
        build_chunks(args.size, args.overlap)


if __name__ == '__main__':
    main()
