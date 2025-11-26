from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

from app.core.config import settings


@contextmanager
def get_conn():
    """
    Простой способ работы с БД:
    - на каждую операцию открываем соединение
    - коммит/роллбек делаем автоматически
    """
    conn = psycopg2.connect(settings.db_dsn, cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
