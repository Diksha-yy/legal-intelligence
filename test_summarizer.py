
from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m3_summarization.summarizer import summarize_text


# Enter the PDF path
pdf_path = input("Enter your PDF file path: ").strip().strip('"')

# Module 1: Extract text
document = extract_pdf_text(pdf_path)

print("\nOCR extraction completed.")

# Module 3: Generate summary
result = summarize_text(document["full_text"])

print("\n========== LEGAL DOCUMENT SUMMARY ==========\n")

print(result["summary"])

print("\n========== MODEL INFORMATION ==========")
print("Model:", result["model"])
print("Device:", result["device"])
print("Chunks processed:", result["chunks_processed"])