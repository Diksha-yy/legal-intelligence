
from pathlib import Path

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m6_risk_scoring.risk_scorer import calculate_risk


pdf_path = input("Enter full PDF file path: ").strip().strip('"')

if not Path(pdf_path).is_file():
    raise FileNotFoundError("PDF file not found.")

# Module 1: Extract text
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

# Module 6: Calculate screening score
result = calculate_risk(
    document["full_text"],
    document_types[choice]
)

print("\n========== LEGAL RISK REPORT ==========")

print("\nDocument type:", result["document_type"])
print("Screening score:", result["risk_score"], "/ 100")
print("Screening band:", result["risk_level"])

print("\nFindings:")

for index, finding in enumerate(result["findings"], start=1):
    print(f"\n{index}. {finding['issue']}")
    print("Reason:", finding["reason"])
    print("Weight:", finding["weight"])
    print("Type:", finding["type"])

print("\nTotal findings:", result["total_findings"])

print("\nDisclaimer:")
print(result["disclaimer"])