
from datasets import load_dataset
from pathlib import Path

output_dir = Path("data/external_datasets/ledgar")
output_dir.mkdir(parents=True, exist_ok=True)

print("Downloading LEDGAR from LexGLUE...")

dataset = load_dataset(
    "coastalcph/lex_glue",
    "ledgar"
)

print(dataset)

for split_name, split_data in dataset.items():

    output_file = output_dir / f"{split_name}.jsonl"

    split_data.to_json(
        str(output_file),
        orient="records",
        lines=True,
        force_ascii=False
    )

    print(
        f"Saved {split_name}: "
        f"{len(split_data)} examples"
    )

print("LEDGAR download and export complete.")