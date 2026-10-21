from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m2_classification.classifier import (
    classify_document
)

INPUT_DIR = ROOT / "data" / "employment"
OUTPUT_FILE = ROOT / "data" / "training" / "m2_review.csv"

INPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

records = []

for pdf_file in INPUT_DIR.glob("*.pdf"):

    print("Processing:", pdf_file.name)

    extraction_result = extract_pdf_text(str(pdf_file))
    text = extraction_result["full_text"]

    results = classify_document(text)

    for result in results:

        records.append({
            "document_id": pdf_file.stem,
            "clause": result["clause"],
            "suggested_label": result["category"],
            "actual_label": "",
            "source": pdf_file.name
        })

df = pd.DataFrame(
    records,
    columns=[
        "document_id",
        "clause",
        "suggested_label",
        "actual_label",
        "source"
    ]
)

df = df.drop_duplicates(
    subset=["clause"]
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nDataset generated:", OUTPUT_FILE)
print("Total extracted clauses:", len(df))