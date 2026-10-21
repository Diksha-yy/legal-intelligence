import json
import shutil
from pathlib import Path

path = Path("data/legal_knowledge/legal_records.json")

backup = path.with_suffix(".json.bak")
shutil.copy2(path, backup)

records = json.loads(path.read_text(encoding="utf-8"))

updated = 0

for record in records:
    if "Real Estate (Regulation and Development) Act" in record.get("title", ""):
        record["domain"] = "property"
        record["jurisdiction"] = "India"

        if record.get("effective_date") in ("string", ""):
            record["effective_date"] = None

        updated += 1

path.write_text(
    json.dumps(records, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("Updated records:", updated)