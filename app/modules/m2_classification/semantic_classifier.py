from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from .domain_config import DOMAIN_CATEGORIES


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=8)
def get_category_embeddings(domain):
    categories = DOMAIN_CATEGORIES[domain]

    descriptions = list(categories.values())

    embeddings = get_model().encode(
        descriptions,
        normalize_embeddings=True
    )

    return embeddings


def classify_clause_semantic(clause, domain="employment"):

    if domain not in DOMAIN_CATEGORIES:
        raise ValueError(
            f"Unsupported domain: {domain}"
        )

    if not isinstance(clause, str) or not clause.strip():
        return {
            "clause": clause,
            "category": "Unclassified",
            "confidence": 0.0,
            "domain": domain,
            "method": "semantic"
        }

    model = get_model()

    clause_embedding = model.encode(
        [clause],
        normalize_embeddings=True
    )[0]

    category_embeddings = get_category_embeddings(domain)

    similarities = np.dot(
        category_embeddings,
        clause_embedding
    )

    best_index = int(np.argmax(similarities))

    categories = list(DOMAIN_CATEGORIES[domain].keys())

    best_category = categories[best_index]
    similarity = float(similarities[best_index])

    return {
        "clause": clause,
        "category": best_category,
        "confidence": round(similarity, 4),
        "domain": domain,
        "method": "semantic"
    }