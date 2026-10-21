
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------------
# PATH CONFIGURATION
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = BASE_DIR / "evaluation" / "results"
CSV_PATH = RESULTS_DIR / "m1_metrics.csv"

GRAPH_DIR = RESULTS_DIR / "graphs"
GRAPH_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------------
# LOAD EXPERIMENTAL DATA
# ----------------------------------

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"Metrics file not found: {CSV_PATH}\n"
        "Run your OCR evaluation script first."
    )

df = pd.read_csv(CSV_PATH)

if df.empty:
    raise ValueError("No evaluation data found.")

required_columns = [
    "document",
    "pages",
    "CER",
    "WER",
    "Character_Accuracy",
    "Word_Accuracy",
    "Processing_Time"
]

missing = set(required_columns) - set(df.columns)

if missing:
    raise ValueError(
        f"Missing CSV columns: {missing}"
    )

# Ensure numeric columns are valid
numeric_cols = [
    "pages",
    "CER",
    "WER",
    "Character_Accuracy",
    "Word_Accuracy",
    "Processing_Time"
]

df[numeric_cols] = df[numeric_cols].apply(
    pd.to_numeric,
    errors="coerce"
)

df = df.dropna(subset=numeric_cols)

if df.empty:
    raise ValueError("No valid numeric data available.")

print("\nLoaded Evaluation Results:")
print(df.to_string(index=False))


# ----------------------------------
# GRAPH 1: CER AND WER COMPARISON
# ----------------------------------

plt.figure(figsize=(10, 6))

x = range(len(df))
width = 0.35

plt.bar(
    [i - width / 2 for i in x],
    df["CER"] * 100,
    width=width,
    label="CER (%)"
)

plt.bar(
    [i + width / 2 for i in x],
    df["WER"] * 100,
    width=width,
    label="WER (%)"
)

plt.xticks(
    list(x),
    df["document"],
    rotation=30,
    ha="right"
)

plt.xlabel("Test Document")
plt.ylabel("Error Rate (%)")
plt.title("M1 OCR: Character and Word Error Rates")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(
    GRAPH_DIR / "graph1_cer_wer.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ----------------------------------
# GRAPH 2: TEXT ACCURACY
# ----------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    [i - width / 2 for i in x],
    df["Character_Accuracy"],
    width=width,
    label="Character Accuracy (%)"
)

plt.bar(
    [i + width / 2 for i in x],
    df["Word_Accuracy"],
    width=width,
    label="Word Accuracy (%)"
)

plt.xticks(
    list(x),
    df["document"],
    rotation=30,
    ha="right"
)

plt.xlabel("Test Document")
plt.ylabel("Normalized Score (%)")
plt.title("M1 OCR: Character and Word Accuracy")
plt.ylim(bottom=0)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(
    GRAPH_DIR / "graph2_accuracy.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ----------------------------------
# GRAPH 3: PROCESSING TIME
# ----------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["document"],
    df["Processing_Time"]
)

plt.xlabel("Test Document")
plt.ylabel("Processing Time (seconds)")
plt.title("M1 OCR: Document Processing Time")

plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(
    GRAPH_DIR / "graph3_processing_time.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ----------------------------------
# GRAPH 4: PROCESSING TIME VS PAGES
# ----------------------------------

plt.figure(figsize=(8, 6))

plt.scatter(
    df["pages"],
    df["Processing_Time"],
    s=100
)

plt.xlabel("Number of PDF Pages")
plt.ylabel("Processing Time (seconds)")
plt.title("M1 OCR: Processing Time vs Document Size")

# Add document labels to points
for _, row in df.iterrows():
    plt.annotate(
        str(row["document"]),
        (row["pages"], row["Processing_Time"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )

plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    GRAPH_DIR / "graph4_time_vs_pages.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ----------------------------------
# GRAPH 5: OVERALL PERFORMANCE
# ----------------------------------

mean_cer = df["CER"].mean() * 100
mean_wer = df["WER"].mean() * 100

mean_char_accuracy = df["Character_Accuracy"].mean()
mean_word_accuracy = df["Word_Accuracy"].mean()

metrics = [
    "Mean CER",
    "Mean WER",
    "Mean Character Score",
    "Mean Word Score"
]

values = [
    mean_cer,
    mean_wer,
    mean_char_accuracy,
    mean_word_accuracy
]

plt.figure(figsize=(9, 6))

bars = plt.bar(metrics, values)

plt.ylabel("Percentage (%)")
plt.title("M1 OCR: Overall Evaluation Summary")

plt.xticks(rotation=20, ha="right")

for bar, value in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.2f}%",
        ha="center",
        va="bottom"
    )

plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    GRAPH_DIR / "graph5_overall_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ----------------------------------
# SAVE SUMMARY STATISTICS
# ----------------------------------

summary_path = GRAPH_DIR / "m1_summary.txt"

with open(summary_path, "w", encoding="utf-8") as f:

    f.write("M1 OCR PERFORMANCE SUMMARY\n")
    f.write("==========================\n")

    f.write(f"Documents evaluated: {len(df)}\n")
    f.write(f"Total pages: {df['pages'].sum()}\n")

    f.write(f"Mean CER: {mean_cer:.4f}%\n")
    f.write(f"Mean WER: {mean_wer:.4f}%\n")

    f.write(
        f"Mean Character Score: "
        f"{mean_char_accuracy:.2f}%\n"
    )

    f.write(
        f"Mean Word Score: "
        f"{mean_word_accuracy:.2f}%\n"
    )

    f.write(
        f"Mean Processing Time: "
        f"{df['Processing_Time'].mean():.4f} seconds\n"
    )

print("\nAll graphs generated successfully!")

print("Graph folder:", GRAPH_DIR)
print("Summary file:", summary_path)