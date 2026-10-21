
import os
import sys
import time

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, PROJECT_ROOT)

from app.modules.m7_fairness.fairness_analyzer import (
    analyze_fairness
)

# --------------------------------------------------
# Synthetic test document
# --------------------------------------------------

document_type = "employment"

test_document = """
EMPLOYMENT AGREEMENT

The company may terminate the employee without cause.

The company may modify the employment terms at any time.

The employee agrees to indemnify the company against all losses.

A penalty may apply for breach of the agreement.

The employee accepts unlimited liability for all direct and
indirect damages.

The employee agrees to a non-compete obligation.
"""

# Expected indicators drafted from the rules in M7.
# Each indicator has one intended matching phrase.
# These are synthetic reference labels, not expert-validated
# fairness or legal-risk labels.

expected_indicators = [
    "Unilateral termination",
    "Unilateral modification",
    "Broad indemnity",
    "Penalty or financial deduction",
    "Broad liability",
    "Restrictive obligations"
]

# --------------------------------------------------
# Run M7
# --------------------------------------------------

start_time = time.perf_counter()

result = analyze_fairness(
    test_document,
    document_type=document_type
)

elapsed_time = time.perf_counter() - start_time

predicted_indicators = [
    finding["indicator"]
    for finding in result["findings"]
]

expected_set = set(expected_indicators)
predicted_set = set(predicted_indicators)

# --------------------------------------------------
# Indicator-level evaluation
# --------------------------------------------------

true_positive = len(expected_set & predicted_set)

false_positive = len(predicted_set - expected_set)

false_negative = len(expected_set - predicted_set)

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

print("\n========== M7 EVALUATION RESULTS ==========")

print("\nDocument Type:", result["document_type"])

print("Expected Indicators:", len(expected_set))
print("Detected Indicators:", result["total_indicators"])

print("\nExpected Indicators:")
for indicator in expected_indicators:
    print("-", indicator)

print("\nPredicted Indicators:")
for indicator in predicted_set:
    print("-", indicator)

print("\n--- Evaluation Metrics ---")
print("True Positives:", true_positive)
print("False Positives:", false_positive)
print("False Negatives:", false_negative)

print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1_score:.4f}")

print("\n--- Detailed Findings ---")

for index, finding in enumerate(result["findings"], start=1):
    print(f"\nFinding {index}")
    print("Indicator:", finding["indicator"])
    print("Matched Text:", finding["matched_text"])
    print("Excerpt:", finding["clause_excerpt"])
    print("Review Required:", finding["review_required"])

print(f"\nExecution Time: {elapsed_time:.4f} seconds")

print("\nDisclaimer:", result["disclaimer"])

print("\nNote: Single synthetic development test.")
print("Indicators are keyword-based and require human review.")
print("This does not establish legal fairness or enforceability.")

# --------------------------------------------------
# Save results
# --------------------------------------------------

output_dir = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "results"
)

os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(
    output_dir,
    "m7_results.txt"
)

with open(output_file, "w", encoding="utf-8") as f:

    f.write("M7 Fairness Analysis Evaluation\n")
    f.write("=" * 40 + "\n")

    f.write(f"Document Type: {document_type}\n")
    f.write(f"Expected Indicators: {len(expected_set)}\n")
    f.write(f"Detected Indicators: {result['total_indicators']}\n")

    f.write(f"True Positives: {true_positive}\n")
    f.write(f"False Positives: {false_positive}\n")
    f.write(f"False Negatives: {false_negative}\n")

    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1-Score: {f1_score:.4f}\n")
    f.write(f"Execution Time: {elapsed_time:.4f} seconds\n")

    f.write("\nFindings:\n")

    for finding in result["findings"]:
        f.write(
            f"- {finding['indicator']}: "
            f"{finding['matched_text']}\n"
        )

    f.write("\nDisclaimer:\n")
    f.write(result["disclaimer"] + "\n")

print("\nResults saved to:", output_file)