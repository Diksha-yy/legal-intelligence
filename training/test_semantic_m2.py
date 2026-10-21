import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.modules.m2_classification.semantic_classifier import (
    classify_clause_semantic
)


examples = [
    (
        "employment",
        "The employee shall receive an annual performance bonus."
    ),
    (
        "rental",
        "The tenant shall pay a refundable security deposit of Rs. 30000."
    ),
    (
        "property",
        "The seller confirms that the property is free from mortgages."
    ),
    (
        "divorce",
        "Both parties agree to joint custody of their minor child."
    )
]


for domain, clause in examples:

    result = classify_clause_semantic(
        clause,
        domain=domain
    )

    print("\nDomain:", domain)
    print("Clause:", clause)
    print("Category:", result["category"])
    print("Similarity:", result["confidence"])