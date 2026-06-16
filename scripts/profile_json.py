from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

for file in DATA_DIR.glob("*.json"):

    print("\n" + "=" * 60)
    print(file.name)
    print("=" * 60)

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Records:", len(data))

    if data:
        print("\nFields:")

        keys = set()

        for record in data:
            keys.update(record.keys())

        for key in sorted(keys):
            print(" -", key)