from pathlib import Path
import yaml
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INST_ROOT = (
    PROJECT_ROOT.parent
    / "riscv-unified-db"
    / "spec"
    / "std"
    / "isa"
    / "inst"
)

# Grab the first instruction YAML file we find
sample = next(INST_ROOT.rglob("*.yaml"))

print(f"\nFILE:\n{sample}")

with open(sample, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

print("\nFULL YAML CONTENT:\n")
print(json.dumps(data, indent=2, default=str))

print("\n" + "=" * 50)
print("FIELD ANALYSIS")
print("=" * 50)

print("\nDEFINED BY:")
print(data.get("definedBy"))
print("TYPE:", type(data.get("definedBy")))

print("\nHINTS:")
print(data.get("hints"))
print("TYPE:", type(data.get("hints")))

print("\nPSEUDOINSTRUCTIONS:")
print(data.get("pseudoinstructions"))
print("TYPE:", type(data.get("pseudoinstructions")))