from sqlalchemy import text


class DashboardService:

    MONTHLY_FEE = 40

    @staticmethod
    def summary(db):
        query = text("""
            SELECT
              (SELECT COUNT(*) FROM users)    AS users_count,
              (SELECT COUNT(*) FROM members)  AS members_count,
              (SELECT COUNT(*) FROM projects) AS projects_count
        """)
        return db.execute(query).mappings().one()

    @staticmethod
    def projects_by_status(db):
        query = text("""
            SELECT status, COUNT(*) AS total
            FROM projects
            GROUP BY status
            ORDER BY status
        """)
        return db.execute(query).mappings().all()

    @staticmethod
    def recent_activity(db, limit=10):
        query = text("""
            SELECT
              a.created_at,
              u.username,
              a.action,
              a.entity
            FROM audit_log a
            LEFT JOIN users u ON u.id = a.user_id
            ORDER BY a.created_at DESC
            LIMIT :limit
        """)
        return db.execute(
            query,
            {"limit": limit}
        ).mappings().all()

    @staticmethod
    def get_quota_project_id(db):
        row = db.execute(
            text("SELECT id FROM projects WHERE name = 'Cuotas mensuales'")
        ).first()
        return row[0] if row else None

    @staticmethod
    def monthly_financials(db, start_date=None, end_date=None):
        quota_project_id = DashboardService.get_quota_project_id(db)

        sql = """
            WITH active_members AS (
                SELECT COUNT(*) AS total
                FROM members
            )
            SELECT
              date_trunc('month', c.created_at) AS month,
              SUM(c.amount) AS real_amount,
              (am.total * :fee) AS expected_amount
            FROM contributions c
            CROSS JOIN active_members am
            WHERE c.project_id = :quota_project_id
        """

        params = {
            "quota_project_id": quota_project_id,
            "fee": DashboardService.MONTHLY_FEE
        }

        if start_date:
            sql += " AND c.created_at >= :start_date"
            params["start_date"] = start_date

        if end_date:
            sql += " AND c.created_at <= :end_date"
            params["end_date"] = end_date

        sql += " GROUP BY month, am.total ORDER BY month"

        return db.execute(
            text(sql),
            params
        ).mappings().all()
