
from pathlib import Path

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m8_rag.legal_qa import LegalQA


print("LEGAL INTELLIGENCE - MODULE 8")
print("RAG-Based Legal Question Answering")

pdf_path = input(
    "Enter the full PDF file path: "
).strip().strip('"')

if not pdf_path:
    print("Error: Please enter a PDF file path.")
    raise SystemExit

path = Path(pdf_path)

if not path.exists() or not path.is_file():
    print("Error: PDF file not found.")
    raise SystemExit

if path.suffix.lower() != ".pdf":
    print("Error: Please select a PDF file.")
    raise SystemExit

# Extract text using Module 1
print("\nExtracting document text...")

result = extract_pdf_text(str(path))
text = result["full_text"]

if not text.strip():
    print("No text could be extracted.")
    raise SystemExit

print("Document extracted successfully!")

# Initialize RAG system
qa = LegalQA()

# Create vector index
chunk_count = qa.index_document(text)

print(f"\nDocument indexed into {chunk_count} chunks.")

# Ask multiple questions
while True:

    question = input(
        "\nAsk a question about the document "
        "(or type 'exit' to stop): "
    ).strip()

    if question.lower() == "exit":
        print("Exiting Legal Q&A.")
        break

    if not question:
        print("Please enter a question.")
        continue

    try:
        report = qa.ask_question(question)

        print("\n========== ANSWER ==========")
        print(report["answer"])

        print("\n========== SOURCE REFERENCES ==========")

        for source in report["sources"]:
            print(
                f"{source['source']} | "
                f"Similarity: {source['similarity']}"
            )

        print("\nDisclaimer:")
        print(report["disclaimer"])

    except Exception as error:
        print("Error:", error)