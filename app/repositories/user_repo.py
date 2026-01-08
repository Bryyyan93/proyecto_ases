from sqlalchemy import text
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):

    def get_by_username(self, username: str):
        # ARRAY_AGG devuelve una lista de roles
        # Esto te permite multi-rol en el futuro sin tocar el diseño
        query = text("""
            SELECT
                u.person_id,
                u.username,
                u.password_hash,
                p.is_active,
                ARRAY_AGG(r.name) AS roles
            FROM users u
            JOIN persons p ON p.id = u.person_id
            JOIN user_roles ur ON ur.user_id = u.id
            JOIN roles r ON r.id = ur.role_id
            WHERE u.username = :username
              AND p.is_active = true
            GROUP BY u.id, u.username, u.password_hash, p.is_active
        """)

        return self.db.execute(
            query,
            {"username": username}
        ).mappings().first()
