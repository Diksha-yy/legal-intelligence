
from pathlib import Path

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m7_fairness.fairness_analyzer import analyze_fairness


print("LEGAL INTELLIGENCE - MODULE 7")
print("Fairness Analysis")

pdf_path = input("Enter the full PDF file path: ").strip().strip('"')

if not pdf_path:
    print("Error: Please enter a PDF file path.")
    raise SystemExit

path = Path(pdf_path)

if not path.exists() or not path.is_file():
    print("Error: File not found.")
    raise SystemExit

if path.suffix.lower() != ".pdf":
    print("Error: Please select a PDF file.")
    raise SystemExit

result = extract_pdf_text(str(path))

text = result["full_text"]

if not text.strip():
    print("No text could be extracted from the PDF.")
    raise SystemExit

document_type = input(
    "Enter document type "
    "(employment/job_offer/divorce_family/property/rental): "
).strip().lower()

allowed_types = [
    "employment",
    "job_offer",
    "divorce_family",
    "property",
    "rental"
]

if document_type not in allowed_types:
    print("Invalid document type.")
    raise SystemExit

report = analyze_fairness(text, document_type)

print("\n========== FAIRNESS ANALYSIS ==========")

print("Document Type:", report["document_type"])

print("Total Indicators:", report["total_indicators"])

if report["findings"]:

    for index, finding in enumerate(report["findings"], start=1):

        print(f"\nFinding {index}")
        print("Indicator:", finding["indicator"])
        print("Matched Text:", finding["matched_text"])
        print("Explanation:", finding["explanation"])
        print("Clause:", finding["clause_excerpt"])
        print("Human Review Required:", finding["review_required"])

else:
    print("No configured indicators were detected.")

print("\nDisclaimer:")
print(report["disclaimer"])