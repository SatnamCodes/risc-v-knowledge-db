import json
from pathlib import Path

from db import get_connection

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "csrs.json"

conn = get_connection()
cur = conn.cursor()

with open(DATA_FILE, "r", encoding="utf-8") as f:
    csrs = json.load(f)

count = 0
field_count = 0

for csr in csrs:

    address = csr.get("address")
    length = csr.get("length")

    cur.execute(
        """
        INSERT INTO csrs (
            name,
            long_name,
            address,
            description,
            priv_mode,
            length,
            writable,
            virtual_address
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING csr_id
        """,
        (
            csr.get("name"),
            csr.get("long_name"),
            str(address) if address is not None else None,
            csr.get("description"),
            csr.get("priv_mode"),
            str(length) if length is not None else None,
            csr.get("writable"),
            csr.get("virtual_address"),
        ),
    )

    csr_id = cur.fetchone()[0]

    fields = csr.get("fields") or {}

    for field_name, field_info in fields.items():

        field_description = None
        if isinstance(field_info, dict):
            field_description = field_info.get("description")
            if not isinstance(field_description, (str, type(None))):
                field_description = json.dumps(field_description)

        cur.execute(
            """
            INSERT INTO csr_fields (
                csr_id,
                field_name,
                field_description
            )
            VALUES (%s,%s,%s)
            """,
            (
                csr_id,
                field_name,
                field_description,
            ),
        )

        field_count += 1

    count += 1

conn.commit()

print(f"Loaded CSRs: {count}")
print(f"Loaded CSR fields: {field_count}")

cur.close()
conn.close()
