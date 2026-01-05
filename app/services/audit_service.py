from sqlalchemy import text


class AuditService:

    @staticmethod
    def log(db, user_id, action, entity=None, entity_id=None):
        db.execute(
            text("""
                INSERT INTO audit_log
                (user_id, action, entity, entity_id)
                VALUES (:u, :a, :e, :ei)
            """),
            {
                "u": user_id,
                "a": action,
                "e": entity,
                "ei": entity_id
            }
        )
        db.commit()
