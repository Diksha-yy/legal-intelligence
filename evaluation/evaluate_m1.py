import sys
import re
import string
from pathlib import Path

import pymupdf
import sys
import re
import string
import csv
import time

from pathlib import Path
import pymupdf

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.modules.m1_ocr.extractor import extract_pdf_text


EVAL_DIR = BASE_DIR / "evaluation"
DATA_DIR = EVAL_DIR / "reference_docs"
RESULTS_DIR = EVAL_DIR / "results"

DATA_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Synthetic reference text.
# This is a controlled functional test, not a real legal document.
REFERENCE_TEXT = (
    "The employee shall receive a monthly salary of "
    "25000 rupees. The notice period shall be thirty days."
)


def create_test_pdf(pdf_path):
    """Create a digital PDF containing known reference text."""

    doc = pymupdf.open()

    page = doc.new_page()

    page.insert_textbox(
        pymupdf.Rect(50, 50, 550, 300),
        REFERENCE_TEXT,
        fontsize=12
    )

    doc.save(pdf_path)
    doc.close()


def normalize_text(text):
    """Normalize case and whitespace for comparison."""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def levenshtein_distance(a, b):
    """Calculate edit distance using dynamic programming."""

    previous = list(range(len(b) + 1))

    for i, char_a in enumerate(a, start=1):
        current = [i]

        for j, char_b in enumerate(b, start=1):

            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1

            replace_cost = previous[j - 1] + (
                char_a != char_b
            )

            current.append(
                min(insert_cost, delete_cost, replace_cost)
            )

        previous = current

    return previous[-1]


def calculate_error_rates(reference, predicted):

    ref_chars = normalize_text(reference)
    pred_chars = normalize_text(predicted)

    char_errors = levenshtein_distance(
        ref_chars, pred_chars
    )

    cer = char_errors / max(len(ref_chars), 1)

    ref_words = ref_chars.split()
    pred_words = pred_chars.split()

    word_errors = levenshtein_distance(
        ref_words, pred_words
    )

    wer = word_errors / max(len(ref_words), 1)

    return cer, wer


def main():

    pdf_path = DATA_DIR / "m1_synthetic_test.pdf"

    create_test_pdf(pdf_path)

    print("=" * 55)
    print("M1 OCR FUNCTIONAL EVALUATION")
    print("=" * 55)

    # Measure OCR processing time
    start_time = time.perf_counter()

    result = extract_pdf_text(str(pdf_path))

    end_time = time.perf_counter()

    processing_time = end_time - start_time

    extracted_text = result["full_text"]

    cer, wer = calculate_error_rates(
        REFERENCE_TEXT,
        extracted_text
    )
    # Calculate normalized scores for reporting
    char_accuracy = max(0, 1 - cer) * 100
    word_accuracy = max(0, 1 - wer) * 100

    # Save results in CSV format
    csv_path = RESULTS_DIR / "m1_metrics.csv"

    file_exists = csv_path.exists()

    with open(
        csv_path,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "document",
                "pages",
                "CER",
                "WER",
                "Character_Accuracy",
                "Word_Accuracy",
                "Processing_Time"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "document": result["filename"],
            "pages": result["page_count"],
            "CER": round(cer, 6),
            "WER": round(wer, 6),
            "Character_Accuracy": round(char_accuracy, 2),
            "Word_Accuracy": round(word_accuracy, 2),
            "Processing_Time": round(processing_time, 4)
        })

    print("CSV results saved:", csv_path)
    print("Processing time:", round(processing_time, 4), "seconds")

    print("PDF:", result["filename"])
    print("Pages:", result["page_count"])

    print("\nReference text:")
    print(REFERENCE_TEXT)

    print("\nExtracted text:")
    print(extracted_text)

    print("\nCER:", round(cer, 4))
    print("WER:", round(wer, 4))

    print("\nExtraction methods:")

    for page in result["pages"]:
        print(
            "Page", page["page_number"],
            "-", page["extraction_method"]
        )

    output_path = RESULTS_DIR / "m1_results.txt"

    with open(
        output_path, "w", encoding="utf-8"
    ) as file:

        file.write("M1 OCR FUNCTIONAL EVALUATION\n")
        file.write("============================\n")
        file.write(f"PDF: {result['filename']}\n")
        file.write(f"Page count: {result['page_count']}\n")
        file.write(f"CER: {cer:.4f}\n")
        file.write(f"WER: {wer:.4f}\n")
        file.write(
            f"Extracted text: {extracted_text}\n"
        )

    print("\nResults saved to:", output_path)


if __name__ == "__main__":
    main()