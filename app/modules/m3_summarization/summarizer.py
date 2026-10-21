"""Fast preview summarization; sampling is NOT a full-document legal summary."""
from functools import lru_cache
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = 'facebook/bart-large-cnn'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

@lru_cache(maxsize=1)
def _load_model():
    print(f'Loading BART model on {DEVICE}...', flush=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE).eval()
    return tokenizer, model

def split_into_chunks(text, max_tokens=900):
    tokenizer, _ = _load_model()
    tokens = tokenizer.encode(text, add_special_tokens=False)
    return [tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)
            for i in range(0, len(tokens), max_tokens)]

def summarize_text(text, max_length=110, min_length=25, max_chunks=4):
    if not text or not text.strip():
        raise ValueError('Document text is empty.')
    if max_chunks < 1:
        raise ValueError('max_chunks must be >= 1')
    tokenizer, model = _load_model()
    chunks = split_into_chunks(text)
    total = len(chunks)
    if total > max_chunks:
        # Sample across the document rather than silently taking the first pages.
        selected_indices = sorted({round(i * (total - 1) / (max_chunks - 1))
                                   for i in range(max_chunks)}) if max_chunks > 1 else [0]
    else:
        selected_indices = list(range(total))
    summaries = []
    for n, idx in enumerate(selected_indices, 1):
        print(f'Summarizing selected chunk {n}/{len(selected_indices)} (original {idx + 1}/{total})...', flush=True)
        inputs = tokenizer(chunks[idx], return_tensors='pt', truncation=True, max_length=1024)
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
        with torch.inference_mode():
            output = model.generate(**inputs, max_new_tokens=max_length,
                                    min_new_tokens=min(min_length, max_length - 1),
                                    num_beams=2, no_repeat_ngram_size=3, early_stopping=True)
        summaries.append(tokenizer.decode(output[0], skip_special_tokens=True))
    partial = len(selected_indices) < total
    return {
        'summary': '\n\n'.join(summaries),
        'chunks_processed': len(selected_indices),
        'total_chunks': total,
        'selected_chunk_numbers': [i + 1 for i in selected_indices],
        'coverage': 'sampled_preview' if partial else 'all_chunks',
        'warning': ('Sampled preview only: omitted chunks may contain important legal terms. '
                    'Do not use this as a complete legal summary.') if partial else None,
        'model': MODEL_NAME,
        'device': DEVICE,
    }
