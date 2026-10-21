import json
import re
from collections import defaultdict

INPUT = "processed/pages.jsonl"

documents = defaultdict(list)

with open(INPUT, encoding="utf-8") as f:
    for line in f:
        if line.strip():
            row = json.loads(line)
            documents[row["document_id"]].append(row)

for doc_id in ["RENT_001", "DIV_001", "PROP_001", "EMP_001"]:
    print(f"\n{'=' * 20} {doc_id} {'=' * 20}")

    matches = []

    for row in documents[doc_id]:
        lines = row["text"].splitlines()

        for index, line in enumerate(lines):
            cleaned = line.strip()

            if re.match(
                r"^(?:SECTION\s+)?1\s*[.:\-–]\s+[A-Za-z]",
                cleaned,
                re.IGNORECASE
            ):
                context = " | ".join(
                    x.strip()
                    for x in lines[index:index + 3]
                )

                matches.append((row["page"], context[:180]))

    for page, context in matches[:12]:
        print(f"Page {page}: {context}")

    if not matches:
        print("No matching Section 1 headings found.")