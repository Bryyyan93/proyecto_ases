-- PERSONS (root entity)
-- Entidad raíz del dominio.
-- Representa a la persona real, independientemente de sus roles
-- (usuario del sistema, miembro económico, ambos o ninguno).
CREATE TABLE persons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- USERS (subtype)
-- Especialización de persons.
-- Contiene únicamente información relacionada con autenticación
-- y acceso al sistema.
-- PK compartida con persons para garantizar integridad semántica.
CREATE TABLE users (
    person_id UUID PRIMARY KEY REFERENCES persons(id) ON DELETE CASCADE,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- ROLES
CREATE TABLE roles (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- USER ↔ ROLES
CREATE TABLE user_roles (
    user_id UUID NOT NULL REFERENCES users(person_id) ON DELETE CASCADE,
    role_id SMALLINT NOT NULL REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);

-- SESSIONS
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(person_id) ON DELETE CASCADE,
    login_at TIMESTAMP NOT NULL DEFAULT now(),
    logout_at TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- AUDIT LOG
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(person_id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    entity TEXT NOT NULL,
    entity_id UUID,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

