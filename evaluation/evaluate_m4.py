import sys
import time
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.modules.m4_translation.translator import (
    translate_text
)

from sacrebleu.metrics import BLEU, CHRF


RESULTS_DIR = BASE_DIR / "evaluation" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Synthetic English input
SOURCE_TEXT = (
    "The employee will receive a monthly salary "
    "of 25000 rupees. The employee must provide "
    "thirty days notice before termination."
)


# Illustrative draft references only.
# Obtain fluent-speaker review before research use.
REFERENCES = {
    "Hindi": (
        "कर्मचारी को हर महीने 25000 रुपये वेतन मिलेगा। "
        "नौकरी समाप्त करने से पहले कर्मचारी को "
        "तीस दिन का नोटिस देना होगा।"
    ),
    "Marathi": (
        "कर्मचाऱ्याला दरमहा 25000 रुपये पगार मिळेल. "
        "नोकरी संपवण्यापूर्वी कर्मचाऱ्याला "
        "तीस दिवसांची नोटीस द्यावी लागेल."
    )
}


def main():

    bleu_metric = BLEU()
    chrf_metric = CHRF()

    output_path = RESULTS_DIR / "m4_results.txt"

    print("=" * 55)
    print("M4 TRANSLATION EVALUATION")
    print("=" * 55)

    all_results = []

    for language in ["Hindi", "Marathi"]:

        print(f"\nEvaluating English to {language}")

        start_time = time.perf_counter()

        result = translate_text(
            SOURCE_TEXT,
            target_language=language
        )

        elapsed = time.perf_counter() - start_time

        translated_text = result["translated_text"]
        reference = REFERENCES[language]

        bleu_score = bleu_metric.corpus_score(
            [translated_text],
            [[reference]]
        )

        chrf_score = chrf_metric.corpus_score(
            [translated_text],
            [[reference]]
        )

        print("\nSource:")
        print(SOURCE_TEXT)

        print("\nReference translation:")
        print(reference)

        print("\nModel translation:")
        print(translated_text)

        print("\nBLEU:", round(bleu_score.score, 4))
        print("chrF++:", round(chrf_score.score, 4))
        print("Inference time:", round(elapsed, 4), "seconds")

        all_results.append({
            "language": language,
            "translation": translated_text,
            "bleu": bleu_score.score,
            "chrf": chrf_score.score,
            "time": elapsed,
            "model": result["model"]
        })

    with open(
        output_path, "w", encoding="utf-8"
    ) as file:

        file.write("M4 TRANSLATION EVALUATION\n")
        file.write("=========================\n\n")

        file.write("Source text:\n")
        file.write(SOURCE_TEXT + "\n\n")

        file.write(
            "NOTE: Reference translations are illustrative "
            "drafts requiring fluent-speaker review.\n\n"
        )

        for item in all_results:

            file.write(
                f"Target language: {item['language']}\n"
            )
            file.write(
                f"Translation: {item['translation']}\n"
            )
            file.write(
                f"BLEU: {item['bleu']:.4f}\n"
            )
            file.write(
                f"chrF++: {item['chrf']:.4f}\n"
            )
            file.write(
                f"Inference time: {item['time']:.4f} seconds\n"
            )
            file.write(
                f"Model: {item['model']}\n\n"
            )

    print("\nResults saved to:", output_path)


if __name__ == "__main__":
    main()