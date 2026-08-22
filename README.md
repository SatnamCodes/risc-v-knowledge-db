# RISC-V Knowledge DB

A small, queryable database built from the RISC-V Unified DB.

The RISC-V specs are precise, but the useful facts are spread across many YAML
files: instructions, extensions, CSRs, encodings, pseudoinstructions, privilege
metadata, and prose. This project pulls the parts I care about into a simpler
shape:

```text
riscv-unified-db YAML -> JSON snapshots -> PostgreSQL tables
```

The goal is not to replace Unified DB. The goal is to make it easier to ask
questions.

Examples:

- Which extension defines an instruction?
- What is the encoding and assembly form for an opcode?
- Which CSRs exist, at what address, and in which privilege mode?
- Which instructions have pseudoinstruction expansions?
- What does the local RISC-V ISA surface look like as relational data?

## Current Snapshot

Generated from `riscv-unified-db/spec/std/isa`.

| Dataset | Records |
| --- | ---: |
| Extensions | 164 |
| Instructions | 1351 |
| CSRs | 396 |

The extracted JSON files live in `data/`.

## Repo Layout

```text
risc-v-db/
  data/
    extensions.json
    instructions.json
    csrs.json
  scripts/
    db.py
    extract_extensions.py
    extract_instructions.py
    extract_csrs.py
    load_extensions.py
    load_instructions.py
    load_csrs.py
    query.py
    verify_pipeline.py
    inventory.py
    profile_json.py
    dev/            # one-off exploration scripts used while reverse-engineering the YAML shape
  sql/
    schema.sql
    queries.sql
```

`riscv-unified-db/` is expected to sit next to this repo:

```text
RISC-V/
  risc-v-db/
  riscv-unified-db/
```

## Data Model

The schema is intentionally boring.

- `extensions`: extension name, kind, type, description, company, source file
- `extension_versions`: version/state/ratification metadata
- `extension_requirements`: extension dependency edges
- `instructions`: name, assembly, format, kind, encoding, operation text
- `pseudoinstructions`: conditional instruction rewrites
- `instruction_hints`: hint references attached to instructions
- `csrs`: CSR name, address, privilege mode, length, access flags
- `csr_fields`: named fields inside CSRs

See `sql/schema.sql` for the full DDL.

## Setup

Start by cloning both repos into the same parent folder. This matters because
the scripts look for `../riscv-unified-db` relative to this project.

```bash
mkdir RISC-V
cd RISC-V

git clone https://github.com/riscv/riscv-unified-db.git
git clone https://github.com/SatnamCodes/risc-v-knowledge-db.git risc-v-db

cd risc-v-db
```

You should end up with:

```text
RISC-V/
  risc-v-db/
  riscv-unified-db/
```

Create a Postgres database:

```bash
createdb riscv_knowledge_db
psql riscv_knowledge_db < sql/schema.sql
```

Install Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your local Postgres connection
details (host, database, user, password). `scripts/db.py` loads this file for
every loader and query script, so nothing is hardcoded in the scripts
themselves. `.env` is gitignored.

```bash
cp .env.example .env
```

## Generate Data

From `risc-v-db/`:

```bash
python scripts/extract_extensions.py
python scripts/extract_instructions.py
python scripts/extract_csrs.py
```

This reads Unified DB YAML and writes normalized JSON snapshots into `data/`.

Useful inspection commands:

```bash
python scripts/inventory.py
python scripts/profile_json.py
```

## Load Postgres

Load extensions first, because instructions reference them by name:

```bash
python scripts/load_extensions.py
python scripts/load_instructions.py
python scripts/load_csrs.py
```

Then sanity-check row counts against expected minimums:

```bash
python scripts/verify_pipeline.py
```

## Query the Data

`sql/queries.sql` has example SQL for the questions this project set out to
answer (which extension defines an instruction, CSRs by privilege mode, which
instructions have pseudoinstructions, extension dependency chains, etc.):

```bash
psql riscv_knowledge_db -f sql/queries.sql
```

For a quick lookup without writing SQL, there's also a small CLI:

```bash
python scripts/query.py instruction addi
python scripts/query.py csr mstatus
python scripts/query.py extension Zfa
```

## Notes

This is a learning and systems project: take a large hardware spec corpus, make
it tractable, then query it like normal data.

The code favors explicit scripts over framework glue. That makes the pipeline
easy to inspect, debug, and extend. If a field is missing or weird, the source
YAML path is carried through as `_source_file`, so the raw spec entry is still
one hop away.

## License

MIT. See `LICENSE`.
