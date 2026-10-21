
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Pretrained multilingual translation model
MODEL_NAME = "facebook/nllb-200-distilled-600M"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading translation model on {DEVICE}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

model.to(DEVICE)
model.eval()

print("Translation model loaded successfully!")


# Supported target languages
LANGUAGES = {
    "Hindi": "hin_Deva",
    "Marathi": "mar_Deva"
}


def translate_text(text, target_language="Hindi"):
    """
    Translate English text into Hindi or Marathi.
    """

    if not text or not text.strip():
        raise ValueError("Input text is empty.")

    if target_language not in LANGUAGES:
        raise ValueError(
            "Supported languages: Hindi, Marathi"
        )

    target_code = LANGUAGES[target_language]

    # Set source language to English
    tokenizer.src_lang = "eng_Latn"

    # Split text into manageable chunks
    words = text.split()
    chunks = []

    current_chunk = []
    word_count = 0

    for word in words:
        current_chunk.append(word)
        word_count += 1

        if word_count >= 100:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            word_count = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    translated_chunks = []

    # Target language token
    target_token_id = tokenizer.convert_tokens_to_ids(
        target_code
    )

    for index, chunk in enumerate(chunks, start=1):

        print(f"Translating chunk {index}/{len(chunks)}...")

        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        inputs = {
            key: value.to(DEVICE)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            output_tokens = model.generate(
                **inputs,
                forced_bos_token_id=target_token_id,
                max_length=512,
                num_beams=4
            )

        translated_text = tokenizer.batch_decode(
            output_tokens,
            skip_special_tokens=True
        )[0]

        translated_chunks.append(translated_text)

    final_translation = "\n".join(translated_chunks)

    return {
        "source_language": "English",
        "target_language": target_language,
        "translated_text": final_translation,
        "model": MODEL_NAME
    }