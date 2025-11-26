import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt


_ALGO = "pbkdf2_sha256"
_ITERATIONS = 200_000  # для MVP норм; если будет тормозить — можно 100_000
_SALT_BYTES = 16


def _b64e(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


def _b64d(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode((s + pad).encode("utf-8"))


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(_SALT_BYTES)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    # формат хранения: algo$iterations$salt$hash
    return f"{_ALGO}${_ITERATIONS}${_b64e(salt)}${_b64e(dk)}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        algo, iters_s, salt_s, hash_s = stored_hash.split("$", 3)
        if algo != _ALGO:
            return False

        iters = int(iters_s)
        salt = _b64d(salt_s)
        expected = _b64d(hash_s)

        dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iters)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def create_access_token(data: dict, secret_key: str, algorithm: str, expires_minutes: int) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload["exp"] = expire
    return jwt.encode(payload, secret_key, algorithm=algorithm)
