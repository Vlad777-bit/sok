from app.auth.repository import UserRepository
from app.auth.security import hash_password, verify_password
from app.core.config import settings


def seed_admin() -> None:
    """
    Если пароль/хэш менялся (например, раньше был bcrypt) — обновим.
    """
    repo = UserRepository()
    existing = repo.get_by_username(settings.admin_username)

    desired_hash = hash_password(settings.admin_password)

    if not existing:
        repo.create(
            username=settings.admin_username,
            password_hash=desired_hash,
            role="ADMIN",
        )
        return

    # если пароль не проходит проверку (или формат хэша старый) — перезаписываем
    if not verify_password(settings.admin_password, existing["password_hash"]):
        repo.update_password(
            username=settings.admin_username,
            password_hash=desired_hash,
            role="ADMIN",
        )
