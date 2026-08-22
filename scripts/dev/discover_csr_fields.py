from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSR_ROOT = (
    PROJECT_ROOT.parent
    / "riscv-unified-db"
    / "spec"
    / "std"
    / "isa"
    / "csr"
)

all_keys = set()

yaml_count = 0

for file in CSR_ROOT.rglob("*.yaml"):

    try:
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if isinstance(data, dict):
            all_keys.update(data.keys())
            yaml_count += 1

    except Exception as e:
        print(f"Error reading {file}")
        print(e)

print("\nCSR Files Read:", yaml_count)

print("\nFields Found:\n")

for key in sorted(all_keys):
    print(key)