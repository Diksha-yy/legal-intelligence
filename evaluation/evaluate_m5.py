
import os
import sys
import csv
import time

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.m5_missing_clauses.missing_clause import (
    detect_missing_clauses,
    DOMAIN_CHECKLISTS
)

# --------------------------------------------------
# Synthetic test document
# --------------------------------------------------

document_type = "employment"

test_document = """
EMPLOYMENT AGREEMENT

The employee will work as a Software Engineer.
The employee will work 40 hours per week.

The monthly salary will be INR 40,000.
The employee will receive medical insurance benefits.

Both parties must sign this agreement.
The employee must provide necessary background checks.
"""

# Reference checklist:
# These are drafted expected outcomes for this synthetic
# test and should be independently reviewed.

expected_present = [
    "Employment Details",
    "Working Hours",
    "Salary and Compensation",
    "Benefits",
    "Conditions and Background Checks",
    "Acceptance and Signatures"
]

expected_missing = [
    "Termination and Notice",
    "Confidentiality"
]

# --------------------------------------------------
# Run M5
# --------------------------------------------------

start_time = time.perf_counter()

result = detect_missing_clauses(
    test_document,
    document_type=document_type
)

elapsed_time = time.perf_counter() - start_time

predicted_present = result["detected_clauses"]
predicted_missing = result["potentially_missing_clauses"]

# --------------------------------------------------
# Evaluate missing-clause detection
# --------------------------------------------------

expected_missing_set = set(expected_missing)
predicted_missing_set = set(predicted_missing)

true_positive = len(
    expected_missing_set & predicted_missing_set
)

false_positive = len(
    predicted_missing_set - expected_missing_set
)

false_negative = len(
    expected_missing_set - predicted_missing_set
)

precision = (
    true_positive / (true_positive + false_positive)
    if true_positive + false_positive > 0
    else 0.0
)

recall = (
    true_positive / (true_positive + false_negative)
    if true_positive + false_negative > 0
    else 0.0
)

f1_score = (
    2 * precision * recall / (precision + recall)
    if precision + recall > 0
    else 0.0
)

# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n========== M5 EVALUATION RESULTS ==========")

print("\nDocument Type:", result["document_type"])

print("\nTotal Expected Clauses:",
      result["total_expected"])

print("Total Detected Clauses:",
      result["total_detected"])

print("Total Potentially Missing:",
      result["total_potentially_missing"])

print("\nExpected Present Clauses:")
for clause in expected_present:
    print("-", clause)

print("\nPredicted Present Clauses:")
for clause in predicted_present:
    print("-", clause)

print("\nExpected Missing Clauses:")
for clause in expected_missing:
    print("-", clause)

print("\nPredicted Missing Clauses:")
for clause in predicted_missing:
    print("-", clause)

print("\n--- Missing-Clause Metrics ---")
print("True Positives:", true_positive)
print("False Positives:", false_positive)
print("False Negatives:", false_negative)

print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1_score:.4f}")

print(f"\nExecution Time: {elapsed_time:.4f} seconds")

print("\nNote: Synthetic development evaluation.")
print("Results depend on the M2 keyword classifier.")
print("Not a legal-compliance or enforceability assessment.")

# --------------------------------------------------
# Save results
# --------------------------------------------------

output_dir = os.path.join(PROJECT_ROOT, "evaluation", "results")
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "m5_results.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write("M5 Missing Clause Detection Evaluation\n")
    f.write("=" * 45 + "\n")
    f.write(f"Document Type: {document_type}\n")
    f.write(f"Total Expected Clauses: {result['total_expected']}\n")
    f.write(f"Total Detected Clauses: {result['total_detected']}\n")
    f.write(
        f"Total Potentially Missing: "
        f"{result['total_potentially_missing']}\n"
    )
    f.write(f"True Positives: {true_positive}\n")
    f.write(f"False Positives: {false_positive}\n")
    f.write(f"False Negatives: {false_negative}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1-Score: {f1_score:.4f}\n")
    f.write(f"Execution Time: {elapsed_time:.4f} seconds\n")
    f.write("\nPredicted Missing Clauses:\n")
    for clause in predicted_missing:
        f.write(f"- {clause}\n")

print("\nResults saved to:", output_file)