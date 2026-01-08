-- Triggers (DESPUÉS de existir tablas y función)
-- Trigger AFTER INSERT/UPDATE/DELETE
-- Llama a la función de auditoría para capturar
-- el estado previo y posterior de la fila.
-- PERSONS
CREATE TRIGGER trg_audit_persons
AFTER INSERT OR UPDATE OR DELETE ON persons
FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();

-- USERS
CREATE TRIGGER trg_audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();

-- MEMBERS
CREATE TRIGGER trg_audit_members
AFTER INSERT OR UPDATE OR DELETE ON members
FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();

-- PROJECTS
CREATE TRIGGER trg_audit_projects
AFTER INSERT OR UPDATE OR DELETE ON projects
FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();

-- CONTRIBUTIONS
CREATE TRIGGER trg_audit_contributions
AFTER INSERT OR UPDATE OR DELETE ON contributions
FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();

-- Trigger de auditoría automática para activities.
-- Garantiza trazabilidad completa del ciclo de vida de las tareas.
CREATE TRIGGER trg_audit_activities
AFTER INSERT OR UPDATE OR DELETE
ON activities
FOR EACH ROW
EXECUTE FUNCTION audit_activities();
