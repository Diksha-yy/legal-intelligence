
from pathlib import Path

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m5_missing_clauses.missing_clause import (
    detect_missing_clauses
)


pdf_path = input("Enter full PDF path: ").strip().strip('"')

if not Path(pdf_path).is_file():
    raise FileNotFoundError("PDF file not found.")

document = extract_pdf_text(pdf_path)

print("\nChoose document type:")
print("1. Employment")
print("2. Job Offer")
print("3. Divorce / Family")
print("4. Property")
print("5. Rental")

choice = input("Enter choice (1-5): ").strip()

document_types = {
    "1": "employment",
    "2": "job_offer",
    "3": "divorce_family",
    "4": "property",
    "5": "rental"
}

if choice not in document_types:
    raise ValueError("Invalid document type.")

result = detect_missing_clauses(
    document["full_text"],
    document_types[choice]
)

print("\n========== MISSING CLAUSE REPORT ==========")

print("\nDocument type:", result["document_type"])

print("\nDetected expected clauses:")
for clause in result["detected_clauses"]:
    print(" -", clause)

print("\nPotentially missing clauses:")
for clause in result["potentially_missing_clauses"]:
    print(" -", clause)

print("\nTotal expected:", result["total_expected"])
print("Detected:", result["total_detected"])
print("Potentially missing:", result["total_potentially_missing"])