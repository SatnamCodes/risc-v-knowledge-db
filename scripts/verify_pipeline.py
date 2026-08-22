"""Sanity check that each table got loaded with a plausible number of rows.
Run after the load_*.py scripts. Exits non-zero on failure, for use in CI.
"""
import sys

from db import get_connection

EXPECTATIONS = {
    "extensions": 100,
    "extension_versions": 100,
    "extension_requirements": 10,
    "instructions": 1000,
    "pseudoinstructions": 10,
    "csrs": 300,
    "csr_fields": 500,
}


def main():
    conn = get_connection()
    cur = conn.cursor()

    failures = []
    for table, minimum in EXPECTATIONS.items():
        cur.execute(f"SELECT count(*) FROM {table}")
        (count,) = cur.fetchone()
        status = "ok" if count >= minimum else "FAIL"
        print(f"{status}: {table} = {count} (expected >= {minimum})")
        if count < minimum:
            failures.append(table)

    cur.close()
    conn.close()

    if failures:
        print(f"\n{len(failures)} table(s) under expected row count: {failures}")
        sys.exit(1)

    print("\nAll tables loaded as expected.")


if __name__ == "__main__":
    main()
