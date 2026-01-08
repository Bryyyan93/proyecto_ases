INSERT INTO roles (id, name, description) VALUES
(1, 'admin', 'Administrador del sistema'),
(2, 'member', 'Miembro de la asociación'),
(3, 'logistica', 'Gestión logística'),
(4, 'informatica', 'Gestión informática'),
(5, 'tesoreria', 'Gestión económica');

INSERT INTO contribution_types (id, name) VALUES
(1, 'monthly_fee'),
(2, 'money'),
(3, 'material'),
(4, 'service');

INSERT INTO activity_statuses (id, name, description, is_final) VALUES
(1, 'planned', 'Actividad planificada', false),
(2, 'in_progress', 'Actividad en curso', false),
(3, 'blocked', 'Actividad bloqueada', false),
(4, 'done', 'Actividad finalizada', true),
(5, 'cancelled', 'Actividad cancelada', true);
