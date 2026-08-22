-- Example queries against the RISC-V knowledge DB.
-- Run after loading data with the scripts/load_*.py scripts.

-- Which extension defines a given instruction?
SELECT i.name, i.assembly, e.name AS extension
FROM instructions i
LEFT JOIN extensions e ON e.extension_id = i.extension_id
WHERE i.name = 'addi';

-- Encoding for a given instruction.
SELECT name, assembly, format, encoding
FROM instructions
WHERE name = 'add.uw';

-- All CSRs in machine mode (M), ordered by address.
SELECT name, long_name, address, length
FROM csrs
WHERE priv_mode = 'M'
ORDER BY address;

-- Fields defined on a given CSR.
SELECT c.name AS csr, f.field_name, f.field_description
FROM csr_fields f
JOIN csrs c ON c.csr_id = f.csr_id
WHERE c.name = 'mstatus'
ORDER BY f.field_name;

-- Instructions that have pseudoinstruction expansions.
SELECT i.name, p.condition, p.translation
FROM pseudoinstructions p
JOIN instructions i ON i.instruction_id = p.instruction_id
ORDER BY i.name;

-- Extension dependency chains: which extensions does X require?
SELECT e.name AS extension, r.required_extension
FROM extension_requirements r
JOIN extensions e ON e.extension_id = r.extension_id
ORDER BY e.name;

-- How many instructions does each extension define?
SELECT e.name AS extension, count(i.instruction_id) AS instruction_count
FROM extensions e
LEFT JOIN instructions i ON i.extension_id = e.extension_id
GROUP BY e.name
ORDER BY instruction_count DESC;

-- Extensions with no ratified version.
SELECT e.name
FROM extensions e
WHERE NOT EXISTS (
    SELECT 1 FROM extension_versions v
    WHERE v.extension_id = e.extension_id
      AND v.state = 'ratified'
);

-- Instructions with no matching extension (data quality check).
SELECT name, source_file
FROM instructions
WHERE extension_id IS NULL;
