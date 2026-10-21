import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


import time
import json
from pathlib import Path

from app.modules.m9_comparison.agreement_comparator import (
    AgreementComparator
)


# --------------------------------------------------
# M9: AGREEMENT COMPARISON - EVALUATION
# --------------------------------------------------

OUTPUT_DIR = Path("evaluation/results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Synthetic example documents
# Document 1: Original agreement
document1 = """
Employment Agreement

The employee will work 40 hours per week.

The monthly salary will be 30000 rupees.

The employee must provide 30 days notice
before leaving the company.

The employee must maintain confidentiality
of company information.
"""


# Document 2: Revised agreement
document2 = """
Employment Agreement

The employee will work 40 hours per week.

The monthly salary will be 35000 rupees.

The employee must provide 60 days notice
before leaving the company.

The employee must maintain confidentiality
of company information.
"""


# --------------------------------------------------
# INITIALIZE COMPARATOR
# --------------------------------------------------

print("Initializing M9 Agreement Comparator...")

comparator = AgreementComparator()


# --------------------------------------------------
# RUN COMPARISON
# --------------------------------------------------

start_time = time.perf_counter()

results = comparator.compare_documents(
    document1,
    document2
)

execution_time = time.perf_counter() - start_time


# --------------------------------------------------
# EVALUATION COUNTS
# --------------------------------------------------

matched_count = len(results["matched_clauses"])

changed_count = len(results["changed_clauses"])

missing_doc2_count = len(
    results["missing_from_document2"]
)

missing_doc1_count = len(
    results["missing_from_document1"]
)


# Expected changes in our synthetic example:
# Salary changed from 30000 to 35000.
# Notice period changed from 30 to 60 days.

expected_changed = 2

expected_missing_doc2 = 0

expected_missing_doc1 = 0


# Count expected changes detected.
# This is a simple development check, not
# a general accuracy measurement.

detected_expected_changes = min(
    changed_count,
    expected_changed
)

change_detection_rate = (
    detected_expected_changes / expected_changed
    if expected_changed > 0
    else 0
)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 50)
print("M9 AGREEMENT COMPARISON RESULTS")
print("=" * 50)

print(
    "Document 1 clauses:",
    results["document1_clause_count"]
)

print(
    "Document 2 clauses:",
    results["document2_clause_count"]
)

print("Matched clauses:", matched_count)

print("Changed clauses:", changed_count)

print(
    "Missing from Document 2:",
    missing_doc2_count
)

print(
    "Missing from Document 1:",
    missing_doc1_count
)

print(
    "Expected changes:",
    expected_changed
)

print(
    "Detected expected changes:",
    detected_expected_changes
)

print(
    "Development change detection rate:",
    round(change_detection_rate * 100, 2),
    "%"
)

print(
    "Execution time:",
    round(execution_time, 4),
    "seconds"
)


# --------------------------------------------------
# SHOW CHANGED CLAUSES
# --------------------------------------------------

print("\nCHANGED CLAUSES:")

for item in results["changed_clauses"]:

    print("\nDocument 1:")
    print(item["document1_clause"])

    print("Document 2:")
    print(item["document2_clause"])

    print(
        "Semantic similarity:",
        item["semantic_similarity"]
    )

    print(
        "Text similarity:",
        item["text_similarity"]
    )


# --------------------------------------------------
# SHOW NUMBER COMPARISON
# --------------------------------------------------

print("\nDOCUMENT 1 NUMBERS:")
print(results["document1_numbers"])

print("\nDOCUMENT 2 NUMBERS:")
print(results["document2_numbers"])


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

output_file = OUTPUT_DIR / "m9_results.txt"

with open(output_file, "w", encoding="utf-8") as file:

    file.write("M9 AGREEMENT COMPARISON EVALUATION\n")
    file.write("=" * 45 + "\n")

    file.write(
        f"Document 1 clauses: "
        f"{results['document1_clause_count']}\n"
    )

    file.write(
        f"Document 2 clauses: "
        f"{results['document2_clause_count']}\n"
    )

    file.write(f"Matched clauses: {matched_count}\n")
    file.write(f"Changed clauses: {changed_count}\n")

    file.write(
        f"Missing from Document 2: "
        f"{missing_doc2_count}\n"
    )

    file.write(
        f"Missing from Document 1: "
        f"{missing_doc1_count}\n"
    )

    file.write(
        f"Expected changes: {expected_changed}\n"
    )

    file.write(
        f"Detected expected changes: "
        f"{detected_expected_changes}\n"
    )

    file.write(
        f"Development change detection rate: "
        f"{change_detection_rate * 100:.2f}%\n"
    )

    file.write(
        f"Execution time: {execution_time:.4f} seconds\n"
    )

    file.write("\nCHANGED CLAUSES:\n")

    for item in results["changed_clauses"]:

        file.write(
            json.dumps(item, indent=2, ensure_ascii=False)
            + "\n"
        )

    file.write("\nDISCLAIMER:\n")
    file.write(results["disclaimer"])

print("\nResults saved to:", output_file)