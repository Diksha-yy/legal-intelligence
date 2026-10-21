
from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m2_classification.classifier import classify_document


pdf_path = input("Enter your PDF file path: ").strip().strip('"')

# Module 1: Extract text
document = extract_pdf_text(pdf_path)

print("\nOCR completed successfully.")

# Module 2: Classify clauses
results = classify_document(document["full_text"])

print("\n========== CLAUSE CLASSIFICATION ==========\n")

for index, result in enumerate(results, start=1):
    print(f"Clause {index}")
    print("Text:", result["clause"])
    print("Category:", result["category"])
    print("Confidence:", result["confidence"])
    print("-" * 50)