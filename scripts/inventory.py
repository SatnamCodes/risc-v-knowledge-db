from pathlib import Path

ROOT = (
    Path(__file__).resolve().parent.parent.parent
    / "riscv-unified-db"
    / "spec"
    / "std"
    / "isa"
)

for folder in sorted(ROOT.iterdir()):
    if folder.is_dir():
        count = len(list(folder.rglob("*.yaml")))
        print(f"{folder.name:<20} {count}")