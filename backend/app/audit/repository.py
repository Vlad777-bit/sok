from app.db.conn import get_conn


class AuditRepository:
    def add(
        self,
        action: str,
        entity: str,
        entity_id: int | None,
        actor: dict | None,
        meta: dict | None = None,
    ) -> None:
        meta = meta or {}

        sql = """
        INSERT INTO audit_logs(
          actor_user_id, actor_username, actor_role,
          action, entity, entity_id, meta
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb);
        """

        actor_user_id = actor["id"] if actor else None
        actor_username = actor["username"] if actor else None
        actor_role = actor["role"] if actor else None

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        actor_user_id,
                        actor_username,
                        actor_role,
                        action,
                        entity,
                        entity_id,
                        meta,
                    ),
                )

    def list_latest(self, limit: int) -> list[dict]:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT %s;",
                    (limit,),
                )
                return cur.fetchall()
