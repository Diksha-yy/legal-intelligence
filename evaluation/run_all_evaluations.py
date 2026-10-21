import os
import sys
import csv
import time
import traceback
from datetime import datetime

# Project root
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, BASE_DIR)

RESULTS_DIR = os.path.join(
    BASE_DIR, "evaluation", "results"
)

os.makedirs(RESULTS_DIR, exist_ok=True)

# Module import checks
MODULES = {
    "M1_OCR": "app.modules.m1_ocr.extractor",
    "M2_Clause_Classification": (
        "app.modules.m2_classification.classifier"
    ),
    "M3_Summarization": (
        "app.modules.m3_summarization.summarizer"
    ),
    "M4_Translation": (
        "app.modules.m4_translation.translator"
    ),
    "M5_Missing_Clause": (
    "app.modules.m5_missing_clauses.missing_clause"
    ),
    "M6_Risk_Scoring": (
        "app.modules.m6_risk_scoring.risk_scorer"
    ),
    "M7_Fairness_Analysis": (
        "app.modules.m7_fairness.fairness_analyzer"
    ),
    "M8_Legal_QA": (
    "app.modules.m8_rag.legal_qa"
    ),
    "M9_Document_Comparison": (
        "app.modules.m9_comparison.agreement_comparator"
    ),
}


def main():
    results = []

    print("=" * 60)
    print("LEGAL INTELLIGENCE - MODULE EVALUATION")
    print("=" * 60)

    for module_name, module_path in MODULES.items():

        print(f"\nChecking {module_name}...")

        start_time = time.perf_counter()

        try:
            __import__(module_path)

            elapsed = time.perf_counter() - start_time

            status = "IMPORT_SUCCESS"
            error = ""

            print(f"Status: {status}")
            print(f"Import time: {elapsed:.4f} seconds")

        except Exception:
            elapsed = time.perf_counter() - start_time

            status = "IMPORT_FAILED"
            error = traceback.format_exc()

            print(f"Status: {status}")
            print(error)

        results.append({
            "module": module_name,
            "module_path": module_path,
            "status": status,
            "import_time_seconds": round(elapsed, 4),
            "error": error
        })

    # Save results
    output_file = os.path.join(
        RESULTS_DIR, "module_import_results.csv"
    )

    with open(
        output_file, "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "module",
                "module_path",
                "status",
                "import_time_seconds",
                "error"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    successful = sum(
        1 for result in results
        if result["status"] == "IMPORT_SUCCESS"
    )

    print("\n" + "=" * 60)
    print(f"Modules imported: {successful}/{len(MODULES)}")
    print(f"Results saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()