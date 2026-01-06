from sqlalchemy import text


class MemberService:

    @staticmethod
    def list_members(db, status="all"):
        query = """
        SELECT
            p.full_name,
            p.email,
            (u.person_id IS NOT NULL) AS is_user,
            u.is_active AS user_active,
            (m.person_id IS NOT NULL) AS is_member,
            BOOL_OR(r.name = 'admin') AS is_admin,
            COALESCE(SUM(c.amount), 0) AS total_contributed
        FROM persons p
        LEFT JOIN users u ON u.person_id = p.id
        LEFT JOIN user_roles ur ON ur.user_id = u.person_id
        LEFT JOIN roles r ON r.id = ur.role_id
        LEFT JOIN members m ON m.person_id = p.id
        LEFT JOIN contributions c ON c.member_id = m.person_id
        """

        conditions = []

        if status == "members":
            conditions.append("m.person_id IS NOT NULL")
        elif status == "active_users":
            conditions.append("u.is_active = true")
        elif status == "admins":
            conditions.append("r.name = 'admin'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += """
        GROUP BY
            p.id, p.full_name, p.email,
            u.person_id, u.is_active,
            m.person_id
        ORDER BY p.full_name
        """

        return db.execute(text(query)).mappings().all()
