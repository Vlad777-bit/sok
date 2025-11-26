from psycopg2.errors import UniqueViolation

from app.auth.repository import UserRepository
from app.auth.security import hash_password
from app.core.config import settings


def seed_admin() -> None:
    """
    Создаём ADMIN, если его ещё нет.
    """
    repo = UserRepository()
    if repo.get_by_username(settings.admin_username):
        return

    try:
        repo.create(
            username=settings.admin_username,
            password_hash=hash_password(settings.admin_password),
            role="ADMIN",
        )
    except UniqueViolation:
        # на случай гонки при перезапуске
        return
