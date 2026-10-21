
import os
import sys
import time

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, PROJECT_ROOT)

from app.modules.m6_risk_scoring.risk_scorer import (
    calculate_risk
)

# --------------------------------------------------
# Synthetic employment agreement
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

# Expected result based on the source-code rules:
#
# Missing Termination and Notice = 15
# Missing Confidentiality = 10
# No placeholders = 0
# Compensation detected = no additional reminder
#
# Expected raw score = 25
#
# This is a rule-derived reference, not an independently
# validated legal-risk label.

expected_score = 25

# --------------------------------------------------
# Run M6
# --------------------------------------------------

start_time = time.perf_counter()

result = calculate_risk(
    test_document,
    document_type=document_type
)

elapsed_time = time.perf_counter() - start_time

actual_score = result["risk_score"]

# --------------------------------------------------
# Compare against rule-derived reference
# --------------------------------------------------

score_difference = abs(actual_score - expected_score)

score_match = actual_score == expected_score

print("\n========== M6 EVALUATION RESULTS ==========")

print("\nDocument Type:", result["document_type"])

print("Expected Score:", expected_score)
print("Actual Risk Score:", actual_score)
print("Absolute Score Difference:", score_difference)
print("Reference Score Match:", score_match)

print("\nRisk Level:", result["risk_level"])

print("\nTotal Findings:", result["total_findings"])

print("\n--- Findings ---")

for index, finding in enumerate(result["findings"], start=1):
    print(f"\nFinding {index}")
    print("Issue:", finding["issue"])
    print("Reason:", finding["reason"])
    print("Weight:", finding["weight"])
    print("Type:", finding["type"])

print(f"\nExecution Time: {elapsed_time:.4f} seconds")

print("\nDisclaimer:", result["disclaimer"])

print("\nNote: Single synthetic development test.")
print("The reference score is derived from configured rules.")
print("This is not independent legal-risk validation.")

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
    "m6_results.txt"
)

with open(output_file, "w", encoding="utf-8") as f:

    f.write("M6 Risk Scoring Evaluation\n")
    f.write("=" * 40 + "\n")

    f.write(f"Document Type: {document_type}\n")
    f.write(f"Expected Score: {expected_score}\n")
    f.write(f"Actual Score: {actual_score}\n")
    f.write(f"Absolute Score Difference: {score_difference}\n")
    f.write(f"Reference Score Match: {score_match}\n")
    f.write(f"Risk Level: {result['risk_level']}\n")
    f.write(f"Total Findings: {result['total_findings']}\n")
    f.write(f"Execution Time: {elapsed_time:.4f} seconds\n")

    f.write("\nFindings:\n")

    for finding in result["findings"]:
        f.write(f"- Issue: {finding['issue']}\n")
        f.write(f"  Weight: {finding['weight']}\n")
        f.write(f"  Type: {finding['type']}\n")

    f.write("\nDisclaimer:\n")
    f.write(result["disclaimer"] + "\n")

print("\nResults saved to:", output_file)