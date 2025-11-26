import psycopg2
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["tech"])

@router.get("/health")
def health() -> dict:
    try:
        conn = psycopg2.connect(settings.db_dsn)
        conn.close()
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "degraded", "db": "error", "details": str(e)}
