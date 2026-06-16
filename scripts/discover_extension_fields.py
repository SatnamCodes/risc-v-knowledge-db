# scripts/discover_extension_fields.py

from pathlib import Path
import json

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "extensions.json"
)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

all_keys = set()

for item in data:
    all_keys.update(item.keys())

print("\nFields found:\n")
for key in sorted(all_keys):
    print(key)