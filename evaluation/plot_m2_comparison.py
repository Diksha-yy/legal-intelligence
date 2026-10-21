from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"

df = pd.read_csv(RESULTS / "m2_model_comparison.csv")

RESULTS.mkdir(exist_ok=True)

# Accuracy comparison
plt.figure(figsize=(8, 5))

plt.bar(
    df["model"],
    df["accuracy"] * 100
)

plt.ylabel("Accuracy (%)")
plt.xlabel("Classification Approach")
plt.title("Clause Classification Accuracy Comparison")
plt.ylim(0, 100)

for i, value in enumerate(df["accuracy"] * 100):
    plt.text(i, value + 1, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.savefig(
    RESULTS / "m2_accuracy_comparison.png",
    dpi=300
)
plt.close()

# Macro-F1 comparison
plt.figure(figsize=(8, 5))

plt.bar(
    df["model"],
    df["macro_f1"] * 100
)

plt.ylabel("Macro-F1 (%)")
plt.xlabel("Classification Approach")
plt.title("Clause Classification Macro-F1 Comparison")
plt.ylim(0, 100)

for i, value in enumerate(df["macro_f1"] * 100):
    plt.text(i, value + 1, f"{value:.2f}%", ha="center")

plt.tight_layout()
plt.savefig(
    RESULTS / "m2_f1_comparison.png",
    dpi=300
)
plt.close()

# Inference time comparison
plt.figure(figsize=(8, 5))

plt.bar(
    df["model"],
    df["mean_ms_per_clause"]
)

plt.ylabel("Mean Inference Time (ms/clause)")
plt.xlabel("Classification Approach")
plt.title("Clause Classification Inference Time")

plt.tight_layout()
plt.savefig(
    RESULTS / "m2_inference_time.png",
    dpi=300
)
plt.close()

print("Research graphs generated successfully.")