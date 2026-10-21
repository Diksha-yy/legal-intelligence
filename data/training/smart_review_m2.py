from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "training" / "m2_selected_for_review.csv"
OUTPUT = ROOT / "data" / "training" / "m2_smart_review.csv"

df = pd.read_csv(INPUT).fillna("")

# Provisional labels only — not verified ground truth
df["proposed_label"] = df["suggested_label"]

# Prioritize unclassified and ambiguous examples
df["review_priority"] = df["suggested_label"].apply(
    lambda x: "HIGH" if x == "Unclassified" else "NORMAL"
)

# User fills this only when a proposed label is wrong
df["corrected_label"] = ""

# Mark reviewed examples explicitly
df["reviewed"] = ""

columns = [
    "document_id",
    "clause",
    "suggested_label",
    "proposed_label",
    "review_priority",
    "corrected_label",
    "reviewed"
]

df = df[columns]

df = df.sort_values(
    by="review_priority",
    ascending=True
)

if OUTPUT.exists():
    raise FileExistsError(
        f"{OUTPUT} already exists. Back it up before regenerating."
    )

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("Smart review file created:", OUTPUT)
print("Total clauses:", len(df))
print("High-priority clauses:",
      (df["review_priority"] == "HIGH").sum())