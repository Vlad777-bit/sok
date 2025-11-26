from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.auth.repository import UserRepository
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = UserRepository().get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_employee(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] not in ("EMPLOYEE", "ADMIN"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return user

def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user
