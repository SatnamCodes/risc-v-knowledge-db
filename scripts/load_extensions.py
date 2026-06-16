import json
import psycopg2
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "extensions.json"

conn = psycopg2.connect(
    host="localhost",
    dbname="riscv_knowledge_db",
    user="totallynotsatnam",
    password="riscv123"
)

cur = conn.cursor()

with open(DATA_FILE, "r", encoding="utf-8") as f:
    extensions = json.load(f)

count = 0

for ext in extensions:

    company = None
    if isinstance(ext.get("company"), dict):
        company = ext["company"].get("name")

    cur.execute("""
        INSERT INTO extensions (
            name,
            long_name,
            description,
            company,
            kind,
            type,
            doc_license,
            rvi_jira_issue,
            source_file
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING extension_id
    """,
    (
        ext.get("name"),
        ext.get("long_name"),
        ext.get("description"),
        company,
        ext.get("kind"),
        ext.get("type"),
        None,
        ext.get("rvi_jira_issue"),
        ext.get("_source_file")
    ))

    extension_id = cur.fetchone()[0]

    for version in ext.get("versions", []):

        cur.execute("""
            INSERT INTO extension_versions (
                extension_id,
                version,
                state,
                ratification_date
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            extension_id,
            version.get("version"),
            version.get("state"),
            version.get("ratification_date")
        ))

    count += 1

conn.commit()

print(f"Loaded {count} extensions")

cur.close()
conn.close()