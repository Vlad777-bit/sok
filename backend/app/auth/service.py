from app.auth.repository import UserRepository
from app.auth.security import verify_password


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str) -> dict | None:
        user = self.repo.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user["password_hash"]):
            return None
        return user
