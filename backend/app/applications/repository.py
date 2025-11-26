from app.db.conn import get_conn


class ApplicationRepository:
    def create(self, data: dict) -> dict:
        sql = """
        INSERT INTO credit_applications (
          client_id, requested_amount, term_months, purpose,
          status, status_changed_at, interest_rate, comment
        )
        VALUES (
          %(client_id)s, %(requested_amount)s, %(term_months)s, %(purpose)s,
          %(status)s, now(), %(interest_rate)s, %(comment)s
        )
        RETURNING *;
        """
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, data)
                return cur.fetchone()

    def get_by_id(self, app_id: int) -> dict | None:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM credit_applications WHERE id = %s;", (app_id,))
                return cur.fetchone()

    def list(self, limit: int, offset: int) -> list[dict]:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM credit_applications ORDER BY id DESC LIMIT %s OFFSET %s;",
                    (limit, offset),
                )
                return cur.fetchall()
