
from pathlib import Path

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m9_comparison.agreement_comparator import (
    AgreementComparator
)


def get_pdf_text(prompt):

    file_path = input(prompt).strip().strip('"')

    if not file_path:
        print("Error: File path cannot be empty.")
        raise SystemExit

    path = Path(file_path)

    if not path.exists() or not path.is_file():
        print("Error: File not found.")
        raise SystemExit

    if path.suffix.lower() != ".pdf":
        print("Error: Please select a PDF file.")
        raise SystemExit

    result = extract_pdf_text(str(path))

    text = result["full_text"]

    if not text.strip():
        print("Error: No text extracted from PDF.")
        raise SystemExit

    return text


print("LEGAL INTELLIGENCE - MODULE 9")
print("Agreement Comparison")

print("\nSelect the first document:")
text1 = get_pdf_text("Enter first PDF path: ")

print("\nSelect the second document:")
text2 = get_pdf_text("Enter second PDF path: ")

comparator = AgreementComparator()

print("\nComparing documents...")
report = comparator.compare_documents(text1, text2)

print("\n========== COMPARISON REPORT ==========")

print(
    "Document 1 clause count:",
    report["document1_clause_count"]
)

print(
    "Document 2 clause count:",
    report["document2_clause_count"]
)

print("\n========== MATCHED CLAUSES ==========")

for item in report["matched_clauses"]:

    print("\nDocument 1:", item["document1_clause"])
    print("Document 2:", item["document2_clause"])
    print("Semantic similarity:", item["similarity"])

print("\n========== CHANGED CLAUSES ==========")

for item in report["changed_clauses"]:

    print("\nOriginal:", item["document1_clause"])
    print("Compared:", item["document2_clause"])

    print(
        "Semantic similarity:",
        item["semantic_similarity"]
    )

    print(
        "Text similarity:",
        item["text_similarity"]
    )

print("\n========== MISSING FROM DOCUMENT 2 ==========")

for clause in report["missing_from_document2"]:
    print("-", clause)

print("\n========== MISSING FROM DOCUMENT 1 ==========")

for clause in report["missing_from_document1"]:
    print("-", clause)

print("\n========== NUMERICAL TERMS ==========")

print("Document 1 numbers:", report["document1_numbers"])
print("Document 2 numbers:", report["document2_numbers"])

print("\nDisclaimer:")
print(report["disclaimer"])