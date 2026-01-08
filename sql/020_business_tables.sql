-- MEMBERS (subtype)
-- Especialización económica de persons.
-- Representa la relación financiera de una persona con la asociación.
CREATE TABLE members (
    person_id UUID PRIMARY KEY REFERENCES persons(id) ON DELETE CASCADE,
    joined_at DATE,
    metadata JSONB
);

-- PROJECTS
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- CONTRIBUTION TYPES
CREATE TABLE contribution_types (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- CONTRIBUTIONS
CREATE TABLE contributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    member_id UUID NOT NULL REFERENCES members(person_id) ON DELETE RESTRICT,
    project_id UUID NOT NULL REFERENCES projects(id),
    type_id SMALLINT NOT NULL REFERENCES contribution_types(id),
    amount NUMERIC,
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
