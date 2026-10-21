import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.modules.m2_classification.hybrid_classifier import (
    classify_clause_hybrid
)

examples = [
    (
        "employment",
        "The employee shall receive a monthly salary of Rs. 50000."
    ),
    (
        "employment",
        "The employee must complete a background verification."
    ),
    (
        "rental",
        "The tenant shall pay a refundable security deposit."
    ),
    (
        "property",
        "The seller confirms that the property has no mortgage."
    ),
    (
        "divorce",
        "Both parties agree on child custody arrangements."
    )
]

for domain, clause in examples:
    result = classify_clause_hybrid(clause, domain)

    print("\nDomain:", domain)
    print("Category:", result["category"])
    print("Method:", result["method"])
    print("Similarity:", result["confidence"])

    if "keyword_category" in result:
        print("Keyword category:", result["keyword_category"])

    if result.get("needs_review"):
        print("⚠ Classifiers disagree")