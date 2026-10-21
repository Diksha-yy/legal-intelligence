import re

CLAUSE_KEYWORDS = {

    "Employment Details": [
        "job title",
        "position",
        "beginning on",
        "start date",
        "employment",
        "candidate",
        "appointed",
        "appointment",
        "duties",
        "responsibilities",
        "department",
        "place of work",
        "work location",
        "report to"
    ],

    "Working Hours": [
        "work schedule",
        "working hours",
        "days per week",
        "hours per week",
        "part-time",
        "full-time",
        "overtime",
        "shift",
        "timings",
        "working days",
        "lunch break",
        "work 40 hours"
    ],

    "Salary and Compensation": [
        "compensation",
        "salary",
        "hourly",
        "payable",
        "payment",
        "wages",
        "per hour",
        "deductions",
        "bonus",
        "remuneration",
        "income tax",
        "pay package",
        "appraisal",
        "salary revision"
    ],

    "Benefits": [
        "benefits",
        "employee handbook",
        "insurance",
        "leave",
        "allowances",
        "medical coverage",
        "health plan",
        "meal vouchers",
        "transportation",
        "provident fund",
        "retirement",
        "maternity",
        "paternity"
    ],

    "Conditions and Background Checks": [
        "contingent",
        "background checks",
        "background verification",
        "required documentation",
        "subject to",
        "verification",
        "identity proof",
        "address proof",
        "reference checks",
        "eligibility requirements",
        "educational certificates"
    ],

    "Acceptance and Signatures": [
        "acceptance",
        "accepted",
        "accept",
        "signing",
        "sign",
        "returning this letter",
        "signature",
        "sincerely",
        "confirm your acceptance",
        "accepted in writing"
    ],

    "Termination and Notice": [
        "termination",
        "terminate",
        "notice period",
        "resignation",
        "resign",
        "dismissal",
        "end of employment",
        "misconduct",
        "written notice",
        "end employment"
    ],

    "Confidentiality": [
        "confidentiality",
        "confidential",
        "non-disclosure",
        "proprietary information",
        "trade secrets",
        "not disclose",
        "unauthorized disclosure",
        "non-public information",
        "protect confidential information"
    ]
}


def split_into_clauses(text):

    if not text:
        return []

    clauses = re.split(
        r"\n\s*\n|\r\n\s*\r\n",
        text
    )

    if len(clauses) == 1:
        clauses = text.splitlines()

    return [
        clause.strip()
        for clause in clauses
        if clause.strip()
    ]


def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def classify_clause(clause):

    text = normalize_text(clause)

    scores = {}

    for category, keywords in CLAUSE_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            pattern = (
                r"(?<!\w)"
                + re.escape(keyword)
                + r"(?!\w)"
            )

            if re.search(pattern, text):
                score += 1

        if score > 0:
            scores[category] = score

    if not scores:

        return {
            "clause": clause,
            "category": "Unclassified",
            "confidence": 0.0
        }

    best_category = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_category]

    total_score = sum(scores.values())

    confidence = (
        best_score / total_score
        if total_score > 0
        else 0.0
    )

    return {
        "clause": clause,
        "category": best_category,
        "confidence": round(confidence, 2)
    }


def classify_document(text):

    clauses = split_into_clauses(text)

    return [
        classify_clause(clause)
        for clause in clauses
    ]