CREATE TABLE extensions (
    extension_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    long_name TEXT,
    description TEXT,
    company VARCHAR(255),
    kind VARCHAR(100),
    type VARCHAR(100),
    doc_license VARCHAR(255),
    rvi_jira_issue VARCHAR(255),
    source_file TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE extension_versions (
    version_id SERIAL PRIMARY KEY,
    extension_id INTEGER NOT NULL
        REFERENCES extensions(extension_id)
        ON DELETE CASCADE,

    version VARCHAR(50),
    state VARCHAR(50),
    ratification_date VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE extension_requirements (
    requirement_id SERIAL PRIMARY KEY,

    extension_id INTEGER NOT NULL
        REFERENCES extensions(extension_id)
        ON DELETE CASCADE,

    required_extension VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE instructions (
    instruction_id SERIAL PRIMARY KEY,

    name VARCHAR(100) UNIQUE NOT NULL,
    long_name TEXT,

    assembly TEXT,
    description TEXT,

    format TEXT,
    kind VARCHAR(100),

    encoding TEXT,

    data_independent_timing BOOLEAN,

    extension_id INTEGER
        REFERENCES extensions(extension_id),

    operation_text TEXT,

    source_file TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pseudoinstructions (
    pseudo_id SERIAL PRIMARY KEY,

    instruction_id INTEGER NOT NULL
        REFERENCES instructions(instruction_id)
        ON DELETE CASCADE,

    condition TEXT,
    translation TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE instruction_hints (
    hint_id SERIAL PRIMARY KEY,

    instruction_id INTEGER NOT NULL
        REFERENCES instructions(instruction_id)
        ON DELETE CASCADE,

    hint_reference TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE csrs (
    csr_id SERIAL PRIMARY KEY,

    name VARCHAR(100) UNIQUE NOT NULL,
    long_name TEXT,

    address VARCHAR(20),

    description TEXT,

    priv_mode VARCHAR(10),

    length VARCHAR(20),

    writable BOOLEAN,

    virtual_address INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE csr_fields (
    field_id SERIAL PRIMARY KEY,

    csr_id INTEGER NOT NULL
        REFERENCES csrs(csr_id)
        ON DELETE CASCADE,

    field_name VARCHAR(100),

    field_description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_extension_name
ON extensions(name);

CREATE INDEX idx_instruction_name
ON instructions(name);

CREATE INDEX idx_csr_name
ON csrs(name);