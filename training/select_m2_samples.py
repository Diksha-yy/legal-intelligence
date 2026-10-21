from pathlib import Path
import pandas as pd
import re

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "training" / "m2_review.csv"
OUTPUT = ROOT / "data" / "training" / "m2_selected_for_review.csv"

df = pd.read_csv(INPUT)

required = {
    "document_id",
    "clause",
    "suggested_label"
}

if not required.issubset(df.columns):
    raise ValueError(f"Missing columns: {required - set(df.columns)}")

df = df.dropna(subset=list(required)).copy()

df["clause"] = df["clause"].astype(str).str.strip()
df["word_count"] = df["clause"].str.split().str.len()

# Filter obvious short fragments and extremely long passages
df = df[
    (df["word_count"] >= 8) &
    (df["word_count"] <= 150)
].copy()

# Remove common page-number-only fragments
df = df[
    ~df["clause"].str.fullmatch(r"[\d\s\-./]+", na=False)
]

# Remove duplicate text regardless of capitalization
df["normalized"] = (
    df["clause"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
)

df = df.drop_duplicates(subset=["normalized"])

# Sample across documents rather than taking only the first rows
samples = []

for label, group in df.groupby("suggested_label"):

    group = group.sample(frac=1, random_state=42)

    # First pass: one example per document
    first_pass = group.drop_duplicates(subset=["document_id"])

    # Up to 35 examples for each suggested category
    selected = first_pass.head(35)

    remaining = group.drop(index=selected.index)
    needed = max(0, 35 - len(selected))

    if needed:
        selected = pd.concat([
            selected,
            remaining.head(needed)
        ])

    samples.append(selected)

selected_df = pd.concat(samples, ignore_index=True)

selected_df["actual_label"] = ""

selected_df = selected_df[
    [
        "document_id",
        "clause",
        "suggested_label",
        "actual_label"
    ]
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

if OUTPUT.exists():
    raise FileExistsError(
        f"{OUTPUT} already exists. Rename or back up the reviewed file "
        "before generating a new sample."
    )

selected_df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

print("\n===== SAMPLE SELECTION COMPLETED =====")
print("Filtered candidate segments:", len(df))
print("Selected for review:", len(selected_df))

print("\nSuggested label distribution:")
print(selected_df["suggested_label"].value_counts())

print("\nSaved to:", OUTPUT)