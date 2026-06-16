from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ROOT = (
    PROJECT_ROOT.parent
    / "riscv-unified-db"
    / "spec"
    / "std"
    / "isa"
    / "inst"
)

all_keys = set()

for file in ROOT.rglob("*.yaml"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if isinstance(data, dict):
            all_keys.update(data.keys())

    except Exception:
        pass

for key in sorted(all_keys):
    print(key)