from app.modules.m1_ocr.extractor import extract_pdf_text

pdf_path = input("Enter the PDF file path: ")

result = extract_pdf_text(pdf_path)

print("\nFile:", result["filename"])
print("Pages:", result["page_count"])

for page in result["pages"]:
    print("\nPage:", page["page_number"])
    print("Method:", page["extraction_method"])
    print("Extracted Text:")
    print(page["text"][:1000])