CREATE TABLE members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    email TEXT,
    joined_at DATE,
    metadata JSONB
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE contribution_types (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE contributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    member_id UUID NOT NULL REFERENCES members(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    type_id SMALLINT NOT NULL REFERENCES contribution_types(id),
    amount NUMERIC,
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
