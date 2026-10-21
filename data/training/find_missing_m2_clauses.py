from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "training" / "m2_review.csv"
OUTPUT = ROOT / "data" / "training" / "m2_missing_category_candidates.csv"

df = pd.read_csv(INPUT)

KEYWORDS = {
    "Working Hours": [
        "working hours", "work schedule", "shift",
        "overtime", "hours per week", "working days",
        "weekly hours", "workday", "work week"
    ],
    "Confidentiality": [
        "confidential", "non-disclosure", "trade secret",
        "proprietary", "disclose", "sensitive information"
    ],
    "Acceptance and Signatures": [
        "signature", "signatory", "acceptance",
        "accepted", "execute this agreement",
        "signed by"
    ],
    "Termination and Notice": [
        "terminate", "termination", "resignation",
        "notice period", "dismissal", "separation",
        "written notice"
    ]
}

records = []

for _, row in df.iterrows():

    clause = str(row["clause"])
    text = clause.lower()

    word_count = len(clause.split())

    if not 8 <= word_count <= 150:
        continue

    for category, keywords in KEYWORDS.items():

        if any(keyword in text for keyword in keywords):

            records.append({
                "document_id": row["document_id"],
                "clause": clause,
                "candidate_category": category,
                "actual_label": ""
            })

            break

result = pd.DataFrame(
    records,
    columns=[
        "document_id",
        "clause",
        "candidate_category",
        "actual_label"
    ]
)

result = result.drop_duplicates(subset=["clause"])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

if OUTPUT.exists():
    raise FileExistsError(
        f"{OUTPUT} already exists. Back it up before rerunning."
    )

result.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\nMissing-category candidates:", len(result))
print("\nCategory distribution:")
print(result["candidate_category"].value_counts())
print("\nSaved:", OUTPUT)