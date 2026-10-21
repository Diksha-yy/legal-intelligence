from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "training" / "m2_review.csv"

print("Starting dataset quality check...", flush=True)

if not FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {FILE}")

df = pd.read_csv(FILE)

print("\n========== DATASET QUALITY REPORT ==========")

print("Total extracted segments:", len(df))
print("Unique documents:", df["document_id"].nunique())

print("\nSuggested label distribution:")
print(df["suggested_label"].value_counts(dropna=False))

print("\nMissing clauses:", df["clause"].isna().sum())
print("Duplicate clauses:", df["clause"].duplicated().sum())

df["word_count"] = (
    df["clause"]
    .fillna("")
    .astype(str)
    .str.split()
    .str.len()
)

print("\nShort segments (< 5 words):")
print((df["word_count"] < 5).sum())

print("\nLong segments (> 200 words):")
print((df["word_count"] > 200).sum())

print("\n========== SAMPLE CLAUSES ==========")

print(
    df[["clause", "suggested_label"]]
    .sample(min(10, len(df)), random_state=42)
    .to_string(index=False)
)

print("\nDataset quality check completed!")