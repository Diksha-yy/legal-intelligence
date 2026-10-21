
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


# Pretrained embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class LegalQA:

    def __init__(self):
        print("Loading legal document embedding model...")

        self.model = SentenceTransformer(EMBEDDING_MODEL)

        self.chunks = []
        self.index = None

        print("Embedding model loaded successfully!")

    def split_text(self, text, chunk_size=180, overlap=40):
        """
        Split document text into overlapping word chunks.
        """

        words = text.split()

        if not words:
            return []

        chunks = []
        start = 0

        while start < len(words):

            end = min(start + chunk_size, len(words))

            chunk = " ".join(words[start:end])

            chunks.append(chunk)

            if end == len(words):
                break

            start = end - overlap

        return chunks

    def index_document(self, text):

        if not text or not text.strip():
            raise ValueError("Document text cannot be empty.")

        self.chunks = self.split_text(text)

        if not self.chunks:
            raise ValueError("No usable text chunks found.")

        print(f"Creating embeddings for {len(self.chunks)} chunks...")

        embeddings = self.model.encode(
            self.chunks,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        dimension = embeddings.shape[1]

        # Inner product on normalized embeddings
        # gives cosine similarity.
        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        print("Document indexed successfully!")

        return len(self.chunks)

    def ask_question(self, question, top_k=3):

        if self.index is None:
            raise ValueError(
                "Please index a document before asking questions."
            )

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

        k = min(top_k, len(self.chunks))

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        retrieved_chunks = []

        for rank, (score, idx) in enumerate(
            zip(scores[0], indices[0]),
            start=1
        ):

            if idx < 0:
                continue

            retrieved_chunks.append({
                "source": f"Chunk {idx + 1}",
                "text": self.chunks[idx],
                "similarity": round(float(score), 4),
                "rank": rank
            })

        # Extractive answer:
        # Return relevant passages from the document.
        answer_parts = []

        for item in retrieved_chunks:
            answer_parts.append(
                f"[{item['source']}]\n{item['text']}"
            )

        answer = "\n\n".join(answer_parts)

        return {
            "question": question,
            "answer": answer,
            "sources": retrieved_chunks,
            "disclaimer": (
                "This is a document-grounded prototype. "
                "The retrieved text is not a legal opinion. "
                "Similarity scores are not confidence scores "
                "or measures of legal correctness. "
                "Verify answers against the original document."
            )
        }