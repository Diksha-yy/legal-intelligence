import json
from collections import defaultdict
from pathlib import Path

INPUT = Path("processed/pages.jsonl")

stats = defaultdict(lambda: {
    "pages": 0,
    "characters": 0,
    "empty_pages": 0,
    "short_pages": 0
})

with INPUT.open("r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue

        row = json.loads(line)

        doc_id = row["document_id"]
        text = row.get("text") or ""

        stats[doc_id]["pages"] += 1
        stats[doc_id]["characters"] += len(text)

        if not text.strip():
            stats[doc_id]["empty_pages"] += 1

        if len(text.strip()) < 100:
            stats[doc_id]["short_pages"] += 1

print("\nLEGAL DATASET QUALITY REPORT")
print("-" * 75)

for doc_id, data in sorted(stats.items()):
    print(
        f"{doc_id:10} | "
        f"Pages: {data['pages']:3} | "
        f"Characters: {data['characters']:8} | "
        f"Empty: {data['empty_pages']:2} | "
        f"Short: {data['short_pages']:2}"
    )

print("-" * 75)

print("Total documents:", len(stats))
print("Total pages:", sum(x["pages"] for x in stats.values()))
print("Total characters:", sum(x["characters"] for x in stats.values()))
print("Total empty pages:", sum(x["empty_pages"] for x in stats.values()))