from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

# один контекст хэширования на всё приложение
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # bcrypt принимает максимум 72 байта
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Пароль слишком длинный для bcrypt (макс. 72 байта). Сделайте короче.")
    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, secret_key: str, algorithm: str, expires_minutes: int) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["exp"] = expire
    return jwt.encode(payload, secret_key, algorithm=algorithm)
