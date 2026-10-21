import sys
import time
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.modules.m3_summarization.summarizer import (
    summarize_text
)

from rouge_score import rouge_scorer


RESULTS_DIR = BASE_DIR / "evaluation" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# Synthetic employment document
DOCUMENT_TEXT = """
This employment agreement is between ABC Technologies
and the employee.

The employee will work as a software developer.
The employee will receive a monthly salary of
25000 rupees.

The employee will work eight hours per day,
five days per week.

The employee must maintain confidentiality
of company information.

Either party must provide thirty days notice
to terminate the employment agreement.
"""


# Draft reference summary.
# Manually review before using as gold-standard data.
REFERENCE_SUMMARY = (
    "The employee will work as a software developer "
    "at ABC Technologies, receive a monthly salary "
    "of 25000 rupees, work eight hours per day, "
    "maintain confidentiality, and provide or receive "
    "thirty days notice for termination."
)


def main():

    print("=" * 55)
    print("M3 SUMMARIZATION EVALUATION")
    print("=" * 55)

    start_time = time.perf_counter()

    result = summarize_text(
        DOCUMENT_TEXT,
        max_length=100,
        min_length=20
    )

    elapsed = time.perf_counter() - start_time

    generated_summary = result["summary"]

    # ROUGE evaluation
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL"],
        use_stemmer=True
    )

    scores = scorer.score(
        REFERENCE_SUMMARY,
        generated_summary
    )

    print("\nReference summary:")
    print(REFERENCE_SUMMARY)

    print("\nGenerated summary:")
    print(generated_summary)

    print("\nROUGE Results:")

    for metric, score in scores.items():
        print(
            f"{metric}: "
            f"Precision={score.precision:.4f}, "
            f"Recall={score.recall:.4f}, "
            f"F1={score.fmeasure:.4f}"
        )

    print("\nProcessing Information:")
    print("Model:", result["model"])
    print("Device:", result["device"])
    print("Chunks processed:", result["chunks_processed"])
    print("Inference time:", round(elapsed, 4), "seconds")

    # Save results
    output_path = RESULTS_DIR / "m3_results.txt"

    with open(
        output_path, "w", encoding="utf-8"
    ) as file:

        file.write("M3 SUMMARIZATION EVALUATION\n")
        file.write("===========================\n\n")

        file.write("Reference summary:\n")
        file.write(REFERENCE_SUMMARY + "\n\n")

        file.write("Generated summary:\n")
        file.write(generated_summary + "\n\n")

        for metric, score in scores.items():
            file.write(
                f"{metric}: "
                f"Precision={score.precision:.4f}, "
                f"Recall={score.recall:.4f}, "
                f"F1={score.fmeasure:.4f}\n"
            )

        file.write(f"\nModel: {result['model']}\n")
        file.write(f"Device: {result['device']}\n")
        file.write(
            f"Chunks processed: {result['chunks_processed']}\n"
        )
        file.write(
            f"Inference time: {elapsed:.4f} seconds\n"
        )

    print("\nResults saved to:", output_path)


if __name__ == "__main__":
    main()