import pymupdf
import pytesseract

from PIL import Image
from pathlib import Path


def extract_pdf_text(pdf_path, languages="eng"):
    """
    Extract text from a PDF.
    Uses PyMuPDF for digital PDFs and Tesseract OCR
    for scanned pages.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    results = {
        "filename": pdf_path.name,
        "page_count": 0,
        "pages": [],
        "full_text": ""
    }

    document = pymupdf.open(pdf_path)

    try:
        results["page_count"] = len(document)

        for page_number, page in enumerate(document, start=1):

            # Step 1: Extract digital PDF text
            text = page.get_text("text").strip()

            method = "Digital Text Extraction"

            # Step 2: Use OCR if the page has little text
            if len(text) < 30:

                pix = page.get_pixmap(
                    dpi=300,
                    colorspace=pymupdf.csRGB,
                    alpha=False
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                text = pytesseract.image_to_string(
                    image,
                    lang=languages
                ).strip()

                method = "Tesseract OCR"

            # Step 3: Save page results
            results["pages"].append({
                "page_number": page_number,
                "text": text,
                "extraction_method": method
            })

        # Step 4: Combine all pages
        results["full_text"] = "\n\n".join(
            page["text"] for page in results["pages"]
        )

    finally:
        document.close()

    return results