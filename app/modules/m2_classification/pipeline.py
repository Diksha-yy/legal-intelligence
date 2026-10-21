from .document_detector import detect_document_domain
from .hybrid_classifier import classify_clause_hybrid
from .clause_splitter import split_legal_clauses
from .domain_config import DOMAIN_CATEGORIES


def analyze_document_clauses(text, domain=None):

    detection = detect_document_domain(text)

    if domain is None:
        domain = detection["domain"]

    if domain not in DOMAIN_CATEGORIES:
        return {
            "domain": "unknown",
            "domain_detection": detection,
            "total_clauses": 0,
            "clauses": [],
            "error": "Unable to identify a supported document domain."
        }

    clauses = split_legal_clauses(text)
    
    results = []

    for clause in clauses:
        if not isinstance(clause, str) or not clause.strip():
            continue

        result = classify_clause_hybrid(
            clause,
            domain=domain
        )

        results.append(result)

    return {
        "domain": domain,
        "domain_detection": detection,
        "total_clauses": len(results),
        "clauses": results
    }