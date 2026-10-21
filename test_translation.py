
from pathlib import Path

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m4_translation.translator import translate_text


# Step 1: Get a valid PDF path
while True:
    pdf_path = input(
        "Enter the FULL PDF file path: "
    ).strip().strip('"')

    if not pdf_path:
        print("Error: Please enter a PDF file path.")
        continue

    pdf_path = Path(pdf_path)

    if not pdf_path.is_file():
        print("Error: PDF file not found.")
        print("Check the file name and path.")
        continue

    if pdf_path.suffix.lower() != ".pdf":
        print("Error: Please select a .pdf file.")
        continue

    break


# Step 2: Extract PDF text
document = extract_pdf_text(str(pdf_path))

print("\nPDF text extracted successfully.")


# Step 3: Select language
while True:
    language = input(
        "Enter target language (Hindi or Marathi): "
    ).strip().title()

    if language in ["Hindi", "Marathi"]:
        break

    print("Please enter Hindi or Marathi.")


# Step 4: Translate text
result = translate_text(
    document["full_text"],
    target_language=language
)


# Step 5: Display result
print("\n========== TRANSLATION ==========\n")

print(result["translated_text"])

print("\nTarget language:", result["target_language"])
print("Model:", result["model"])