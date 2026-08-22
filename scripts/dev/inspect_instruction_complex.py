# scripts/inspect_instruction_complex.py

from pathlib import Path
import json

DATA = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "instructions.json"
)

with open(DATA, "r", encoding="utf-8") as f:
    instructions = json.load(f)

for inst in instructions:
    if "definedBy" in inst:
        print("\nDEFINED BY:")
        print(inst["definedBy"])
        break

for inst in instructions:
    if "pseudoinstructions" in inst:
        print("\nPSEUDOINSTRUCTIONS:")
        print(inst["pseudoinstructions"])
        break

for inst in instructions:
    if "hints" in inst:
        print("\nHINTS:")
        print(inst["hints"])
        break