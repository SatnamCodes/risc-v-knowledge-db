from pathlib import Path
import yaml
import json

ROOT = (
    Path(__file__).resolve().parent.parent.parent
    / "riscv-unified-db"
    / "spec"
    / "std"
    / "isa"
    / "ext"
)

sample = next(ROOT.rglob("*.yaml"))

print("FILE:")
print(sample)

with open(sample, "r") as f:
    data = yaml.safe_load(f)

print("\nTYPE:")
print(type(data))

print("\nCONTENT:")
print(json.dumps(data, indent=2, default=str))