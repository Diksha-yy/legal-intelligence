
from app.modules.m2_classification.classifier import classify_document


# Expected clauses for each document type
DOMAIN_CHECKLISTS = {
    "employment": [
        "Employment Details",
        "Working Hours",
        "Salary and Compensation",
        "Benefits",
        "Conditions and Background Checks",
        "Acceptance and Signatures",
        "Termination and Notice",
        "Confidentiality"
    ],

    "job_offer": [
        "Employment Details",
        "Salary and Compensation",
        "Working Hours",
        "Acceptance and Signatures",
        "Benefits"
    ],

    "divorce_family": [
        "Parties and Identification",
        "Property and Asset Division",
        "Financial Support",
        "Child Custody",
        "Visitation Arrangements",
        "Signatures"
    ],

    "property": [
        "Parties and Identification",
        "Property Description",
        "Ownership Details",
        "Sale Consideration",
        "Payment Terms",
        "Possession Details",
        "Signatures"
    ],

    "rental": [
        "Parties and Identification",
        "Property Description",
        "Rent and Payment Terms",
        "Security Deposit",
        "Lease Duration",
        "Maintenance Responsibilities",
        "Termination and Notice",
        "Signatures"
    ]
}


def detect_missing_clauses(text, document_type="employment"):
    """
    Identify expected clause categories that were
    not detected in the document.

    This is a checklist-based screening tool.
    """

    if not text or not text.strip():
        raise ValueError("Document text is empty.")

    if document_type not in DOMAIN_CHECKLISTS:
        raise ValueError(
            "Unsupported document type. Choose: "
            + ", ".join(DOMAIN_CHECKLISTS.keys())
        )

    # Classify document clauses using Module 2
    classifications = classify_document(text)

    detected_categories = {
        item["category"]
        for item in classifications
    }

    expected_categories = DOMAIN_CHECKLISTS[document_type]

    # Find expected categories not detected
    missing = [
        category
        for category in expected_categories
        if category not in detected_categories
    ]

    present = [
        category
        for category in expected_categories
        if category in detected_categories
    ]

    return {
        "document_type": document_type,
        "expected_clauses": expected_categories,
        "detected_clauses": present,
        "potentially_missing_clauses": missing,
        "total_expected": len(expected_categories),
        "total_detected": len(present),
        "total_potentially_missing": len(missing)
    }