
import re


# Prototype indicators that may require human review.
# These are not legal conclusions or validated fairness criteria.

FAIRNESS_RULES = {
    "Unilateral termination": {
        "patterns": [
            r"sole discretion.*terminate",
            r"terminate.*without cause",
            r"terminate.*at any time",
            r"company may terminate",
        ],
        "explanation": (
            "The clause may give one party termination rights "
            "that are not clearly matched by equivalent rights."
        ),
    },

    "Unilateral modification": {
        "patterns": [
            r"modify.*at any time",
            r"change.*without prior notice",
            r"amend.*sole discretion",
            r"unilaterally modify",
        ],
        "explanation": (
            "The clause may allow one party to change terms "
            "without clearly requiring agreement from the other party."
        ),
    },

    "Broad indemnity": {
        "patterns": [
            r"indemnify.*all losses",
            r"indemnify.*any and all claims",
            r"hold harmless",
            r"indemnify.*all damages",
        ],
        "explanation": (
            "The indemnity language may create broad obligations "
            "and should be reviewed for scope and limitations."
        ),
    },

    "Penalty or financial deduction": {
        "patterns": [
            r"penalty",
            r"deduct.*salary",
            r"forfeit.*payment",
            r"liquidated damages",
            r"non-refundable.*fee",
        ],
        "explanation": (
            "The clause refers to a penalty, deduction, or forfeiture "
            "that may require review of its conditions and amount."
        ),
    },

    "Broad liability": {
        "patterns": [
            r"unlimited liability",
            r"liable for all losses",
            r"without limitation.*liability",
            r"all direct and indirect damages",
        ],
        "explanation": (
            "The clause may impose broad liability. Review its scope, "
            "exceptions, and any liability limits."
        ),
    },

    "Restrictive obligations": {
        "patterns": [
            r"non-compete",
            r"non compete",
            r"exclusive service",
            r"shall not engage in any other employment",
            r"shall not work for any competitor",
        ],
        "explanation": (
            "The clause may restrict future work or other activities. "
            "Its scope, duration, and applicability need human review."
        ),
    },
}


def analyze_fairness(text, document_type="employment"):

    if not text or not text.strip():
        raise ValueError("Document text cannot be empty.")

    findings = []
    text_lower = text.lower()

    for rule_name, rule_data in FAIRNESS_RULES.items():

        for pattern in rule_data["patterns"]:

            matches = list(
                re.finditer(pattern, text_lower)
            )

            for match in matches:

                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 150)

                clause_excerpt = text[start:end].strip()

                findings.append({
                    "indicator": rule_name,
                    "matched_text": match.group(),
                    "clause_excerpt": clause_excerpt,
                    "explanation": rule_data["explanation"],
                    "review_required": True,
                })

    # Remove duplicate findings with the same indicator
    # and matched phrase.
    unique_findings = []
    seen = set()

    for finding in findings:

        key = (
            finding["indicator"],
            finding["matched_text"]
        )

        if key not in seen:
            seen.add(key)
            unique_findings.append(finding)

    return {
        "document_type": document_type,
        "total_indicators": len(unique_findings),
        "findings": unique_findings,
        "disclaimer": (
            "This is a preliminary keyword-based analysis. "
            "It does not determine whether a document is fair, "
            "unfair, valid, or enforceable. Results depend on "
            "context and require human review."
        ),
    }