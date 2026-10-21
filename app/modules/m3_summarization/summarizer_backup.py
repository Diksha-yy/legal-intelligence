
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Pretrained BART model
MODEL_NAME = "facebook/bart-large-cnn"

# Use GPU if available, otherwise CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading BART model on {DEVICE}...")


# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model.to(DEVICE)
model.eval()

print("BART model loaded successfully!")


def split_into_chunks(text, max_tokens=900):
    """
    Split long document text into chunks
    within BART's input token limit.
    """

    tokens = tokenizer.encode(
        text,
        add_special_tokens=False
    )

    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]

        chunk_text = tokenizer.decode(
            chunk_tokens,
            skip_special_tokens=True
        )

        if chunk_text.strip():
            chunks.append(chunk_text)

    return chunks


def summarize_text(
    text,
    max_length=150,
    min_length=30
):
    """
    Generate a summary of legal document text.

    Returns a dictionary containing the summary
    and processing information.
    """

    if not text or not text.strip():
        raise ValueError("Document text is empty.")

    chunks = split_into_chunks(text)

    summaries = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {index}/{len(chunks)}...")

        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        inputs = {
            key: value.to(DEVICE)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            summary_ids = model.generate(
                **inputs,
                max_length=max_length,
                min_length=min(
                    min_length,
                    max(5, max_length - 5)
                ),
                num_beams=4,
                length_penalty=2.0,
                early_stopping=True,
                no_repeat_ngram_size=3
            )

        summary = tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )

        summaries.append(summary)

    # Combine the summaries from all chunks
    final_summary = "\n\n".join(summaries)

    return {
        "summary": final_summary,
        "chunks_processed": len(chunks),
        "model": MODEL_NAME,
        "device": DEVICE
    }