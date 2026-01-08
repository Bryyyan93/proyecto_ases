-- Función de auditoría
-- Registra cambios DML a nivel de base de datos
-- independientemente de la aplicación que ejecute la operación.
CREATE OR REPLACE FUNCTION audit_trigger_fn()
RETURNS TRIGGER AS $$
DECLARE
    v_user_id UUID;
BEGIN
    -- Usuario autenticado (puede ser NULL en seeds / scripts)
    BEGIN
        v_user_id := current_setting('app.user_id', true)::UUID;
    EXCEPTION
        WHEN others THEN
            v_user_id := NULL;
    END;

    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (
            user_id,
            action,
            entity,
            entity_id,
            old_data,
            new_data
        )
        VALUES (
            v_user_id,
            TG_OP,
            TG_TABLE_NAME,
            NULL,
            NULL,
            to_jsonb(NEW)
        );
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (
            user_id,
            action,
            entity,
            entity_id,
            old_data,
            new_data
        )
        VALUES (
            v_user_id,
            TG_OP,
            TG_TABLE_NAME,
            NULL,
            to_jsonb(OLD),
            to_jsonb(NEW)
        );
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (
            user_id,
            action,
            entity,
            entity_id,
            old_data,
            new_data
        )
        VALUES (
            v_user_id,
            TG_OP,
            TG_TABLE_NAME,
            NULL,
            to_jsonb(OLD),
            NULL
        );
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Función de auditoría para la tabla activities.
-- Registra INSERT, UPDATE y DELETE.
CREATE OR REPLACE FUNCTION audit_activities()
RETURNS trigger AS $$
BEGIN
    INSERT INTO audit_log (
        user_id,
        action,
        entity,
        entity_id,
        old_data,
        new_data,
        created_at
    )
    VALUES (
        current_setting('app.current_user_id', true)::uuid,
        TG_OP,
        'activities',
        COALESCE(NEW.id, OLD.id),
        CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD) END,
        CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN to_jsonb(NEW) END,
        now()
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
