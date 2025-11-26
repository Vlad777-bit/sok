import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "sok_db")
    db_user: str = os.getenv("DB_USER", "sok_user")
    db_password: str = os.getenv("DB_PASSWORD", "sok_pass")

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "dev_secret_change_me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expires_minutes: int = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "admin123")

    cors_origins_raw: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")

    @property
    def cors_origins(self) -> list[str]:
        # "http://a, http://b" -> ["http://a","http://b"]
        return [x.strip() for x in self.cors_origins_raw.split(",") if x.strip()]

    @property
    def db_dsn(self) -> str:
        return (
            f"host={self.db_host} port={self.db_port} dbname={self.db_name} "
            f"user={self.db_user} password={self.db_password}"
        )

settings = Settings()
