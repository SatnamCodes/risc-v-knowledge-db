from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

ROOT = PROJECT_ROOT / "riscv-unified-db" / "spec" / "std" / "isa"

print("Project root:", PROJECT_ROOT)
print("Looking in:", ROOT)
print("Exists:", ROOT.exists())

if ROOT.exists():
    for folder in sorted(ROOT.iterdir()):
        if folder.is_dir():
            print(folder.name)