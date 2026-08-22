import json
from pathlib import Path

from db import get_connection

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "extensions.json"


def find_required_extensions(node):
    """Recursively pull extension names out of a requirements block,
    which can be a bare {"extension": {...}} or nested under
    allOf/anyOf/oneOf/not."""
    names = []

    if isinstance(node, dict):
        ext = node.get("extension")
        if isinstance(ext, dict) and ext.get("name"):
            names.append(ext["name"])

        for key in ("allOf", "anyOf", "oneOf"):
            for child in node.get(key, []):
                names.extend(find_required_extensions(child))

        if "not" in node:
            names.extend(find_required_extensions(node["not"]))

    return names


conn = get_connection()
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

    for required_name in find_required_extensions(ext.get("requirements")):

        cur.execute("""
            INSERT INTO extension_requirements (
                extension_id,
                required_extension
            )
            VALUES (%s,%s)
        """,
        (
            extension_id,
            required_name
        ))

    count += 1

conn.commit()

print(f"Loaded {count} extensions")

cur.close()
conn.close()