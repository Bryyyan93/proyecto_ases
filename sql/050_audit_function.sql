-- 1. Función de auditoría
CREATE OR REPLACE FUNCTION audit_trigger_fn()
RETURNS TRIGGER AS $$
DECLARE
    v_user_id UUID;
BEGIN
    BEGIN
        v_user_id := current_setting('app.current_user_id')::UUID;
    EXCEPTION WHEN OTHERS THEN
        v_user_id := NULL;
    END;

    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (
            user_id, action, entity, entity_id, old_data, new_data
        )
        VALUES (
            v_user_id, TG_OP, TG_TABLE_NAME, NEW.id, NULL, to_jsonb(NEW)
        );
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (
            user_id, action, entity, entity_id, old_data, new_data
        )
        VALUES (
            v_user_id, TG_OP, TG_TABLE_NAME, NEW.id, to_jsonb(OLD), to_jsonb(NEW)
        );
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (
            user_id, action, entity, entity_id, old_data, new_data
        )
        VALUES (
            v_user_id, TG_OP, TG_TABLE_NAME, OLD.id, to_jsonb(OLD), NULL
        );
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
