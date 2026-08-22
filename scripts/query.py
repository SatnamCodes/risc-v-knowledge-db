"""Small CLI for asking common questions of the loaded RISC-V data
without hand-writing SQL. See sql/queries.sql for the underlying queries.
"""
import argparse

from db import get_connection


def instruction(cur, name):
    cur.execute(
        """
        SELECT i.name, i.assembly, i.description, e.name AS extension
        FROM instructions i
        LEFT JOIN extensions e ON e.extension_id = i.extension_id
        WHERE i.name = %s
        """,
        (name,),
    )
    row = cur.fetchone()
    if not row:
        print(f"No instruction named '{name}'")
        return
    name, assembly, description, extension = row
    print(f"{name}  ({extension or 'unknown extension'})")
    print(f"  assembly: {assembly}")
    if description:
        print(f"  description: {description.strip()}")


def csr(cur, name):
    cur.execute(
        """
        SELECT name, long_name, address, priv_mode, length
        FROM csrs
        WHERE name = %s
        """,
        (name,),
    )
    row = cur.fetchone()
    if not row:
        print(f"No CSR named '{name}'")
        return
    name, long_name, address, priv_mode, length = row
    print(f"{name} - {long_name}")
    print(f"  address: {address}, priv_mode: {priv_mode}, length: {length}")

    cur.execute(
        """
        SELECT field_name FROM csr_fields f
        JOIN csrs c ON c.csr_id = f.csr_id
        WHERE c.name = %s
        ORDER BY field_name
        """,
        (name,),
    )
    fields = [f for (f,) in cur.fetchall()]
    if fields:
        print(f"  fields: {', '.join(fields)}")


def extension(cur, name):
    cur.execute(
        """
        SELECT name, long_name, description, kind, type
        FROM extensions
        WHERE name = %s
        """,
        (name,),
    )
    row = cur.fetchone()
    if not row:
        print(f"No extension named '{name}'")
        return
    name, long_name, description, kind, ext_type = row
    print(f"{name} - {long_name} ({kind}/{ext_type})")

    cur.execute(
        "SELECT count(*) FROM instructions WHERE extension_id = "
        "(SELECT extension_id FROM extensions WHERE name = %s)",
        (name,),
    )
    (count,) = cur.fetchone()
    print(f"  defines {count} instructions")

    cur.execute(
        """
        SELECT required_extension FROM extension_requirements r
        JOIN extensions e ON e.extension_id = r.extension_id
        WHERE e.name = %s
        """,
        (name,),
    )
    requires = [r for (r,) in cur.fetchall()]
    if requires:
        print(f"  requires: {', '.join(requires)}")


COMMANDS = {
    "instruction": instruction,
    "csr": csr,
    "extension": extension,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=COMMANDS.keys())
    parser.add_argument("name")
    args = parser.parse_args()

    conn = get_connection()
    cur = conn.cursor()
    try:
        COMMANDS[args.kind](cur, args.name)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
