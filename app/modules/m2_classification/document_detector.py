from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer

DOMAIN_DESCRIPTIONS = {
    "employment": (
        "Employment agreement, job offer letter, employee salary, "
        "working hours, employer, resignation and termination."
    ),
    "rental": (
        "Residential rental agreement, tenant, landlord, monthly rent, "
        "security deposit, lease and maintenance."
    ),
    "property": (
        "Property sale deed, buyer, seller, ownership, title, "
        "registration, stamp duty and transfer of property."
    ),
    "divorce": (
        "Divorce petition, mutual consent divorce, marriage dissolution, "
        "spousal maintenance, child custody and family court."
    )
}


@lru_cache(maxsize=1)
def get_detector_data():
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    embeddings = model.encode(
        list(DOMAIN_DESCRIPTIONS.values()),
        normalize_embeddings=True
    )

    return model, embeddings


def detect_document_domain(text):
    if not isinstance(text, str) or not text.strip():
        return {
            "domain": "unknown",
            "similarity": 0.0,
            "needs_review": True
        }

    model, domain_embeddings = get_detector_data()

    # Limit extremely long documents
    sample_text = text[:3000]

    embedding = model.encode(
        [sample_text],
        normalize_embeddings=True
    )[0]

    similarities = np.dot(
        domain_embeddings,
        embedding
    )

    best_index = int(np.argmax(similarities))

    domain = list(DOMAIN_DESCRIPTIONS.keys())[best_index]

    return {
        "domain": domain,
        "similarity": round(float(similarities[best_index]), 4),
        "needs_review": False
    }