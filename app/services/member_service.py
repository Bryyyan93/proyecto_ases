from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import uuid

class MemberService:
    @staticmethod
    def create_member(db, full_name, email, is_admin, is_active):
        try:
            # Comprobar email único
            exists = db.execute(
                text("SELECT 1 FROM persons WHERE email = :email"),
                {"email": email}
            ).first()

            if exists:
                raise ValueError("Ya existe una persona con ese email")

            # Crear person
            person_id = str(uuid.uuid4())

            db.execute(
                text("""
                INSERT INTO persons (id, full_name, email, created_at)
                VALUES (:id, :full_name, :email, now())
                """),
                {
                    "id": person_id,
                    "full_name": full_name,
                    "email": email
                }
            )

            # Crear member
            db.execute(
                text("""
                INSERT INTO members (person_id, joined_at, is_active)
                VALUES (:person_id, current_date, :is_active)
                """),
                {
                    "person_id": person_id,
                    "is_active": is_active
                }
            )

            # Crear member
            db.execute(
                text("""
                INSERT INTO users (person_id, username, password_hash, is_active, created_at, updated_at)
                VALUES (:person_id, :username, :password_hash, :is_active, now(), now())
                """),
                {
                    "person_id": person_id,
                    "username": email,
                    "password_hash": '$2b$12$PZqziI5a1hKS.EwMElQhZuet98gPD0u2uEnUxQRKAo4ePXsUpYVzq',
                    "is_active": is_active,
                }
            )

            db.commit()

        except IntegrityError:
            db.rollback()
            raise ValueError("Error de integridad al crear el miembro")

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def list_members(db, status="all"):
        query = """
        SELECT
            p.full_name,
            p.email,
            (u.person_id IS NOT NULL) AS is_user,
            u.is_active AS user_active,
            (m.person_id IS NOT NULL) AS is_member,
            m.is_active AS member_active,
            BOOL_OR(r.name = 'admin') AS is_admin,
            COALESCE(SUM(c.amount), 0) AS total_contributed
        FROM persons p
        LEFT JOIN users u ON u.person_id = p.id
        LEFT JOIN user_roles ur ON ur.user_id = u.person_id
        LEFT JOIN roles r ON r.id = ur.role_id
        LEFT JOIN members m ON m.person_id = p.id
        LEFT JOIN contributions c ON c.member_id = m.person_id
        GROUP BY
            p.id, p.full_name, p.email,
            u.person_id, u.is_active,
            m.person_id, m.is_active
        """

        if status == "active":
            query += " HAVING m.person_id IS NOT NULL AND m.is_active = true"
        elif status == "inactive":
            query += " HAVING m.person_id IS NOT NULL AND m.is_active = false"

        query += " ORDER BY p.full_name"

        return db.execute(text(query)).mappings().all()

