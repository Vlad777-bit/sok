from fastapi import APIRouter

router = APIRouter(tags=["tech"])

@router.get("/ping")
def ping() -> dict:
    return {"message": "pong"}
