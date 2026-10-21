
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
)

# Project root
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.modules.m2_classification.classifier import (
    classify_clause,
    CLAUSE_KEYWORDS,
)

# Input and output files
INPUT_FILE = ROOT / "evaluation" / "m2_test.csv"
OUTPUT_FILE = ROOT / "evaluation" / "m2_predictions.csv"
REPORT_FILE = ROOT / "evaluation" / "m2_metrics.txt"
MATRIX_FILE = ROOT / "evaluation" / "m2_confusion_matrix.csv"

# Use categories from your actual classifier
LABELS = list(CLAUSE_KEYWORDS.keys()) + ["Unclassified"]

# Load test data
df = pd.read_csv(INPUT_FILE)

required_columns = {"clause", "actual_label"}

if not required_columns.issubset(df.columns):
    raise ValueError(
        "CSV must contain clause and actual_label columns."
    )

df = df.dropna(subset=["clause", "actual_label"]).copy()

df["clause"] = df["clause"].astype(str).str.strip()
df["actual_label"] = df["actual_label"].astype(str).str.strip()

if df.empty:
    raise ValueError("No valid test clauses found.")

# Validate labels
invalid = set(df["actual_label"]) - set(LABELS)

if invalid:
    raise ValueError(
        f"Invalid actual labels: {invalid}\n"
        f"Allowed labels: {LABELS}"
    )

# Run your existing classifier
predictions = []

for clause in df["clause"]:
    result = classify_clause(clause)
    predictions.append(result["category"])

df["predicted_label"] = predictions

y_true = df["actual_label"]
y_pred = df["predicted_label"]

# Calculate classification metrics
accuracy = accuracy_score(y_true, y_pred)

precision, recall, f1, support = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=LABELS,
        zero_division=0,
    )
)

# Macro average gives equal importance to each class
macro_precision, macro_recall, macro_f1, _ = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=LABELS,
        average="macro",
        zero_division=0,
    )
)

# Weighted average accounts for class frequency
weighted_precision, weighted_recall, weighted_f1, _ = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=LABELS,
        average="weighted",
        zero_division=0,
    )
)

# Confusion matrix
matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=LABELS,
)

matrix_df = pd.DataFrame(
    matrix,
    index=LABELS,
    columns=LABELS,
)

# Save predictions and matrix
df.to_csv(OUTPUT_FILE, index=False)
matrix_df.to_csv(MATRIX_FILE)

# Generate detailed report
report = classification_report(
    y_true,
    y_pred,
    labels=LABELS,
    zero_division=0,
)

summary = f"""
M2 CLAUSE CLASSIFICATION EVALUATION

Test clauses: {len(df)}

Accuracy:           {accuracy:.4f}
Accuracy (%):       {accuracy * 100:.2f}%

Macro Precision:    {macro_precision:.4f}
Macro Recall:       {macro_recall:.4f}
Macro F1:           {macro_f1:.4f}

Weighted Precision: {weighted_precision:.4f}
Weighted Recall:    {weighted_recall:.4f}
Weighted F1:        {weighted_f1:.4f}

CLASSIFICATION REPORT
{report}

CONFUSION MATRIX
{matrix_df.to_string()}
"""

print(summary)

REPORT_FILE.write_text(summary, encoding="utf-8")

print("\nFiles saved:")
print(OUTPUT_FILE)
print(REPORT_FILE)
print(MATRIX_FILE)