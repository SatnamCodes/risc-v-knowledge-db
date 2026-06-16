from pathlib import Path
import yaml
import json

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIFIED_DB_ROOT = (
    PROJECT_ROOT.parent
    / "riscv-unified-db"
    / "spec"
    / "std"
    / "isa"
    / "csr"
)

OUTPUT_FILE = PROJECT_ROOT / "data" / "csrs.json"
# Ensure data directory exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

csrs = []
failed_files = []

print(f"Reading from: {UNIFIED_DB_ROOT}")

for file in UNIFIED_DB_ROOT.rglob("*.yaml"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if isinstance(data, dict):
            data["_source_file"] = str(file.relative_to(UNIFIED_DB_ROOT))
            csrs.append(data)

    except Exception as e:
        failed_files.append((str(file), str(e)))

print(f"\nLoaded {len(csrs)} csrs")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(csrs, f, indent=2, ensure_ascii=False, default=str)

print(f"Saved to: {OUTPUT_FILE}")

if failed_files:
    print(f"\nFailed files: {len(failed_files)}")
    for file, error in failed_files[:10]:
        print(f"  {file}")
        print(f"    {error}")
