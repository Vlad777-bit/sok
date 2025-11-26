from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import TokenResponse, UserPublic
from app.auth.repository import UserRepository
from app.auth.security import create_access_token
from app.auth.service import AuthService
from app.auth.deps import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

service = AuthService(UserRepository())


@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2 password flow ожидает form-data с полями username/password. :contentReference[oaicite:4]{index=4}
    user = service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expires_minutes=settings.jwt_expires_minutes,
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
def me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "role": current_user["role"],
    }
