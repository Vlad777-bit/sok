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

    @property
    def db_dsn(self) -> str:
        # psycopg2 DSN
        return (
            f"host={self.db_host} port={self.db_port} dbname={self.db_name} "
            f"user={self.db_user} password={self.db_password}"
        )

settings = Settings()
