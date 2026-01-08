-- Catálogo de estados posibles para actividades.
-- Centraliza y controla el ciclo de vida de las tareas.
CREATE TABLE activity_statuses (
    id smallint PRIMARY KEY,
    name text NOT NULL UNIQUE,
    description text,
    is_final boolean NOT NULL DEFAULT false
);

-- Actividades o tareas asociadas a un proyecto.
-- Representan unidades de trabajo planificables y trazables.
CREATE TABLE activities (
    id uuid PRIMARY KEY,
    project_id uuid NOT NULL REFERENCES projects(id),
    status_id smallint NOT NULL REFERENCES activity_statuses(id),
    name text NOT NULL,
    description text,
    start_date date,
    end_date date,
    created_at timestamp NOT NULL
);

-- Asignación de personas a actividades.
-- Se referencia a persons para permitir responsables
-- que no necesariamente sean usuarios del sistema.
CREATE TABLE activity_assignees (
    activity_id uuid NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES persons(id),
    assigned_at timestamp NOT NULL,
    PRIMARY KEY (activity_id, person_id)
);

-- Registro histórico de comentarios y actualizaciones
-- sobre una actividad.
CREATE TABLE activity_logs (
    id bigserial PRIMARY KEY,
    activity_id uuid NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    author_person_id uuid REFERENCES persons(id),
    message text NOT NULL,
    created_at timestamp NOT NULL
);

-- Subdominio de materiales necesarios para una actividad.
-- Ejemplo: paellero, logística, montaje.
CREATE TABLE activity_materials (
    id uuid PRIMARY KEY,
    activity_id uuid NOT NULL REFERENCES activities(id) ON DELETE CASCADE,
    name text NOT NULL,
    quantity numeric,
    unit text,
    notes text
);
