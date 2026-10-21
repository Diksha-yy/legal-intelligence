import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.modules.m2_classification.pipeline import (
    analyze_document_clauses
)

documents = {
    "employment": """
    This employment agreement is between the employer and employee.
    The employee shall receive a monthly salary of Rs. 50000.
    The employee shall work 40 hours per week.
    """,

    "rental": """
    This rental agreement is between landlord and tenant.
    The tenant shall pay monthly rent of Rs. 15000.
    A refundable security deposit of Rs. 30000 is required.
    """,

    "property": """
    This property sale deed is between buyer and seller.
    The seller confirms legal ownership of the property.
    The property is free from mortgages and encumbrances.
    """,

    "divorce": """
    This mutual consent divorce agreement concerns marriage dissolution.
    Both parties agree on child custody arrangements.
    The parties have agreed on financial settlement terms.
    """
}

for expected_domain, text in documents.items():

    result = analyze_document_clauses(text)

    print("\n" + "=" * 50)
    print("Expected Domain:", expected_domain)
    print("Detected Domain:", result["domain"])
    print("Total Clauses:", result["total_clauses"])

    for clause in result["clauses"]:
        print("-", clause["category"])