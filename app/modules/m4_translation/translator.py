"""English passthrough and lazy NLLB loading to reduce CPU/RAM use."""
from functools import lru_cache
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = 'facebook/nllb-200-distilled-600M'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
LANGUAGES = {'Hindi': 'hin_Deva', 'Marathi': 'mar_Deva'}

@lru_cache(maxsize=1)
def _load_model():
    print(f'Loading translation model on {DEVICE}...', flush=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE).eval()
    return tokenizer, model

def translate_text(text, target_language='Hindi'):
    if not text or not text.strip():
        raise ValueError('Input text is empty.')
    language = target_language.strip().capitalize()
    if language == 'English':
        return {'source_language': 'English', 'target_language': 'English',
                'translated_text': text, 'model': 'passthrough'}
    if language not in LANGUAGES:
        raise ValueError('Supported languages: English, Hindi, Marathi')
    tokenizer, model = _load_model()
    tokenizer.src_lang = 'eng_Latn'
    words = text.split()
    chunks = [' '.join(words[i:i + 100]) for i in range(0, len(words), 100)]
    target_id = tokenizer.convert_tokens_to_ids(LANGUAGES[language])
    translated = []
    for i, chunk in enumerate(chunks, 1):
        print(f'Translating chunk {i}/{len(chunks)}...', flush=True)
        inputs = tokenizer(chunk, return_tensors='pt', truncation=True, max_length=512)
        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
        with torch.inference_mode():
            output = model.generate(**inputs, forced_bos_token_id=target_id,
                                    max_new_tokens=256, num_beams=2)
        translated.append(tokenizer.batch_decode(output, skip_special_tokens=True)[0])
    return {'source_language': 'English', 'target_language': language,
            'translated_text': '\n'.join(translated), 'model': MODEL_NAME}
