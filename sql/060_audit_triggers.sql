-- 2. Triggers (DESPUÉS de existir tablas y función)
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
