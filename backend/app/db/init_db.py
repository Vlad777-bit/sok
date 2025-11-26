from pathlib import Path

from app.db.conn import get_conn

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def init_db() -> None:
    """
    Мини-миграции: берём все *.sql по имени, применяем по одному разу.
    """
    MIGRATIONS_DIR.mkdir(parents=True, exist_ok=True)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version TEXT PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
                version = path.name
                cur.execute("SELECT 1 FROM schema_migrations WHERE version = %s;", (version,))
                already = cur.fetchone()
                if already:
                    continue

                sql = path.read_text(encoding="utf-8")
                cur.execute(sql)
                cur.execute("INSERT INTO schema_migrations(version) VALUES (%s);", (version,))
