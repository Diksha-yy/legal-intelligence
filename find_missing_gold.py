import json
import re
from pathlib import Path

path = Path("legal_law_collector/processed/rag_chunks.jsonl")

targets = [
    ("WAGE PAYMENT", "EMP_001", r"payment of wages|time limit for payment|mode of payment"),
    ("PROMOTER DUTIES", "PROP_001", r"obligations of promoter|functions and duties of promoter"),
    ("APARTMENT OWNERSHIP", "PROP_004", r"declaration|common areas and facilities|apartment owner"),
    ("DIVORCE GROUNDS", "DIV_001", r"divorce|adultery|cruelty|desertion"),
    ("FAMILY COURT JURISDICTION", "DIV_003", r"jurisdiction|suits and proceedings"),
]

chunks = []

with path.open(encoding="utf-8") as f:
    for line in f:
        if line.strip():
            chunks.append(json.loads(line))

output = []

for label, document_id, pattern in targets:
    matches = []

    for chunk in chunks:
        if chunk.get("document_id") != document_id:
            continue

        content = chunk.get("text", "")

        if re.search(pattern, content, re.IGNORECASE):
            matches.append(chunk)

    output.append(f"\n{'=' * 70}\n{label}\n{'=' * 70}")

    for chunk in matches[:12]:
        output.append(
            f"\nCHUNK: {chunk['chunk_id']}\n"
            f"TEXT:\n{chunk['text'][:1300]}\n"
        )

result = Path("IEEE_EVIDENCE/current_rag/missing_gold_candidates.txt")
result.parent.mkdir(parents=True, exist_ok=True)
result.write_text("\n".join(output), encoding="utf-8")

print(f"Saved candidates to: {result}")