from app.db.conn import get_conn


class UserRepository:
    def get_by_username(self, username: str) -> dict | None:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
                return cur.fetchone()

    def create(self, username: str, password_hash: str, role: str) -> dict:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users(username, password_hash, role)
                    VALUES (%s, %s, %s)
                    RETURNING id, username, role, created_at;
                    """,
                    (username, password_hash, role),
                )
                return cur.fetchone()

    def update_password(self, username: str, password_hash: str, role: str) -> None:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET password_hash = %s, role = %s
                    WHERE username = %s;
                    """,
                    (password_hash, role, username),
                )
