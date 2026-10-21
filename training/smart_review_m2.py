from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "training" / "m2_selected_for_review.csv"
OUTPUT = ROOT / "data" / "training" / "m2_smart_review.csv"

df = pd.read_csv(INPUT).fillna("")

df["proposed_label"] = df["suggested_label"]

# Prioritize categories with known classification problems
def get_priority(label):
    if label in [
        "Unclassified",
        "Employment Details",
        "Conditions and Background Checks",
        "Termination and Notice"
    ]:
        return "HIGH"
    return "NORMAL"

df["review_priority"] = df["suggested_label"].apply(get_priority)

# Fill these columns during review
df["corrected_label"] = ""
df["reviewed"] = ""

df = df[
    [
        "document_id",
        "clause",
        "proposed_label",
        "review_priority",
        "corrected_label",
        "reviewed"
    ]
]

df = df.sort_values(
    "review_priority",
    ascending=True
)

if OUTPUT.exists():
    raise FileExistsError(
        f"{OUTPUT} already exists. Back it up before rerunning."
    )

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\nSMART REVIEW FILE CREATED")
print("Total clauses:", len(df))
print("High priority:", (df["review_priority"] == "HIGH").sum())
print("Saved:", OUTPUT)