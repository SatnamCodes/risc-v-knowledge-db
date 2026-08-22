from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INST_ROOT = (
    PROJECT_ROOT.parent
    / "riscv-unified-db"
    / "spec"
    / "std"
    / "isa"
    / "inst"
)

types_found = set()

for file in INST_ROOT.rglob("*.yaml"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        defined = data.get("definedBy")

        if defined is not None:
            types_found.add(type(defined).__name__)

    except Exception:
        pass

print(types_found)