
from app.modules.m2_classification.classifier import classify_document
from app.modules.m5_missing_clauses.missing_clause import (
    detect_missing_clauses
)


# Configurable screening weights
RISK_WEIGHTS = {
    "Salary and Compensation": 15,
    "Working Hours": 10,
    "Conditions and Background Checks": 10,
    "Termination and Notice": 15,
    "Confidentiality": 10,
    "Benefits": 5,
    "Acceptance and Signatures": 10,
    "Employment Details": 10
}


def calculate_risk(text, document_type="employment"):
    """
    Calculate an initial rule-based legal risk indicator.

    Higher score means more issues were flagged
    for review. This is NOT a legal opinion.
    """

    if not text or not text.strip():
        raise ValueError("Document text is empty.")

    # Classify clauses using Module 2
    classifications = classify_document(text)

    detected_categories = {
        item["category"]
        for item in classifications
    }

    # Detect potentially missing clauses using Module 5
    missing_report = detect_missing_clauses(
        text,
        document_type
    )

    findings = []
    raw_score = 0

    # Rule 1: Potentially missing expected clauses
    for clause in missing_report["potentially_missing_clauses"]:

        weight = RISK_WEIGHTS.get(clause, 10)

        raw_score += weight

        findings.append({
            "issue": f"Potentially missing: {clause}",
            "reason": (
                "The checklist did not detect this expected "
                "clause category in the document."
            ),
            "weight": weight,
            "type": "Missing clause"
        })

    # Rule 2: Flag placeholder values
    placeholders = [
        "[insert date]",
        "[candidate name]",
        "[candidate address]",
        "[job title]",
        "[company name]",
        "[start date]",
        "[days/hours per week]",
        "[$/hour or salary details]",
        "[acceptance deadline]",
        "[supervisor name, title]"
    ]

    lower_text = text.lower()

    for placeholder in placeholders:
        if placeholder in lower_text:

            weight = 5
            raw_score += weight

            findings.append({
                "issue": f"Unfilled placeholder: {placeholder}",
                "reason": (
                    "The document contains a template placeholder "
                    "that may need to be completed."
                ),
                "weight": weight,
                "type": "Incomplete information"
            })

    # Rule 3: Flag clauses not detected by the classifier
    if "Salary and Compensation" not in detected_categories:
        findings.append({
            "issue": "Compensation details need review",
            "reason": (
                "The classifier did not identify a compensation "
                "clause. Confirm whether payment terms are present."
            ),
            "weight": 0,
            "type": "Review reminder"
        })

    # Limit the score to a 0-100 range
    risk_score = min(100, raw_score)

    # Descriptive bands for this prototype only
    if risk_score <= 25:
        risk_level = "Lower screening score"
    elif risk_score <= 60:
        risk_level = "Moderate screening score"
    else:
        risk_level = "Higher screening score"

    return {
        "document_type": document_type,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "findings": findings,
        "total_findings": len(findings),
        "disclaimer": (
            "This is a preliminary rule-based screening indicator, "
            "not legal advice or a determination of enforceability. "
            "Review the original document and applicable law."
        )
    }