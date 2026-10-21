import json
from datetime import datetime, timezone
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.modules.m1_ocr.extractor import extract_pdf_text


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "data" / "legal_knowledge"
INDEX_DIR = BASE_DIR / "models" / "legal_faiss"

METADATA_FILE = DATA_DIR / "legal_records.json"
INDEX_FILE = INDEX_DIR / "legal_index.faiss"


class LegalKnowledgeBase:

    def __init__(self):

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        INDEX_DIR.mkdir(parents=True, exist_ok=True)

        print("Loading legal knowledge embedding model...")

        self.model = SentenceTransformer(MODEL_NAME)

        self.records = []
        self.index = None

        self.load()

        print("Legal knowledge base ready!")

    def split_text(self, text, chunk_size=180, overlap=40):

        words = text.split()
        chunks = []

        start = 0

        while start < len(words):

            end = min(start + chunk_size, len(words))

            chunks.append(" ".join(words[start:end]))

            if end == len(words):
                break

            start = end - overlap

        return chunks

    def load(self):

        if not METADATA_FILE.exists() or not INDEX_FILE.exists():
            return

        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            self.records = json.load(file)

        self.index = faiss.read_index(str(INDEX_FILE))

        if self.index.ntotal != len(self.records):
            raise ValueError(
                "FAISS index and metadata record count do not match."
            )

    def save(self):

        with open(METADATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.records,
                file,
                indent=2,
                ensure_ascii=False
            )

        if self.index is not None:
            faiss.write_index(
                self.index,
                str(INDEX_FILE)
            )

    def add_legal_document(
        self,
        pdf_path,
        title,
        source_url,
        domain,
        jurisdiction="India",
        effective_date=None,
        version="1"
    ):

        if not title.strip() or not source_url.strip():
            raise ValueError(
                "Official document title and source URL are required."
            )

        result = extract_pdf_text(pdf_path)

        text = result["full_text"]

        if not text.strip():
            raise ValueError("No text extracted from legal document.")

        chunks = self.split_text(text)

        if not chunks:
            raise ValueError("No usable legal text found.")

        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        if self.index is None:

            dimension = embeddings.shape[1]

            self.index = faiss.IndexFlatIP(dimension)

        if self.index.d != embeddings.shape[1]:
            raise ValueError("Embedding dimensions do not match.")

        # Prevent duplicate document-version imports.
        document_key = f"{source_url}|{version}"

        existing_keys = {
            record["document_key"]
            for record in self.records
        }

        if document_key in existing_keys:
            raise ValueError(
                "This document version has already been indexed."
            )

        timestamp = datetime.now(timezone.utc).isoformat()

        for chunk_number, chunk in enumerate(chunks, start=1):

            self.records.append({
                "document_key": document_key,
                "title": title,
                "source_url": source_url,
                "domain": domain,
                "jurisdiction": jurisdiction,
                "effective_date": effective_date,
                "version": version,
                "chunk_number": chunk_number,
                "text": chunk,
                "indexed_at": timestamp,
                "verification_status": "unverified"
            })

        self.index.add(embeddings)

        self.save()

        return {
            "status": "indexed",
            "title": title,
            "version": version,
            "chunks_added": len(chunks),
            "total_chunks": len(self.records),
            "verification_status": "unverified"
        }

    def search(
        self,
        question,
        top_k=5,
        domain=None,
        jurisdiction=None
    ):

        if self.index is None or self.index.ntotal == 0:
            return {
                "question": question,
                "results": [],
                "message": "Legal knowledge base is empty."
            }

        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        # Search all indexed chunks, then filter metadata.
        scores, indices = self.index.search(
            query_embedding,
            self.index.ntotal
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index < 0:
                continue

            record = self.records[int(index)]

            # Domain filtering
            if domain:
                saved_domain = str(
                    record.get("domain") or ""
                ).strip().casefold()

                requested_domain = domain.strip().casefold()

                if saved_domain != requested_domain:
                    continue

            # Jurisdiction filtering
            if jurisdiction:
                saved_jurisdiction = str(
                    record.get("jurisdiction") or ""
                ).strip().casefold()

                requested_jurisdiction = jurisdiction.strip().casefold()

                if saved_jurisdiction != requested_jurisdiction:
                    continue

            # Only records that pass both filters reach this point.
            results.append({
                **record,
                "similarity": round(float(score), 4)
            })

            if len(results) >= top_k:
                break

        return {
            "question": question,
            "results": results,
            "total_results": len(results),
            "disclaimer": (
                "Retrieved legal passages are not legal advice. "
                "Source authenticity, applicability, effective dates "
                "and amendment status require verification."
            )
        }