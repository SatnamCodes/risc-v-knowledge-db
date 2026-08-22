import json
from pathlib import Path

from db import get_connection

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "instructions.json"

conn = get_connection()
cur = conn.cursor()

with open(DATA_FILE, "r", encoding="utf-8") as f:
    instructions = json.load(f)

loaded = 0
missing_extensions = 0

for inst in instructions:

    # -----------------------------------
    # Find extension_id
    # -----------------------------------

    extension_id = None

    defined_by = inst.get("definedBy")

    if isinstance(defined_by, dict):

        ext_info = defined_by.get("extension")

        if isinstance(ext_info, dict):

            ext_name = ext_info.get("name")

            if ext_name:

                cur.execute(
                    """
                    SELECT extension_id
                    FROM extensions
                    WHERE name = %s
                    """,
                    (ext_name,)
                )

                row = cur.fetchone()

                if row:
                    extension_id = row[0]

    if extension_id is None:
        missing_extensions += 1

    # -----------------------------------
    # Insert instruction
    # -----------------------------------

    cur.execute(
        """
        INSERT INTO instructions (
            name,
            long_name,
            assembly,
            description,
            format,
            kind,
            encoding,
            data_independent_timing,
            extension_id,
            operation_text,
            source_file
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING instruction_id
        """,
        (
            inst.get("name"),
            inst.get("long_name"),
            str(inst.get("assembly")),
            inst.get("description"),
            json.dumps(inst.get("format"))
                if inst.get("format") is not None
                else None,
            inst.get("kind"),
            json.dumps(inst.get("encoding"))
                if inst.get("encoding") is not None
                else None,
            inst.get("data_independent_timing"),
            extension_id,
            inst.get("operation()"),
            inst.get("_source_file")
        )
    )

    instruction_id = cur.fetchone()[0]

    # -----------------------------------
    # Pseudoinstructions
    # -----------------------------------

    for pseudo in inst.get("pseudoinstructions", []):

        cur.execute(
            """
            INSERT INTO pseudoinstructions (
                instruction_id,
                condition,
                translation
            )
            VALUES (%s,%s,%s)
            """,
            (
                instruction_id,
                pseudo.get("when"),
                pseudo.get("to")
            )
        )

    # -----------------------------------
    # Hints
    # -----------------------------------
    for hint in inst.get("hints", []):

        cur.execute(
            """
            INSERT INTO instruction_hints (
                instruction_id,
                hint_reference
            )
            VALUES (%s,%s)
            """,
            (
                instruction_id,
                hint.get("$ref")
            )
        )

    loaded += 1

conn.commit()

print(f"Loaded instructions: {loaded}")
print(f"Instructions without extension match: {missing_extensions}")

cur.close()
conn.close()