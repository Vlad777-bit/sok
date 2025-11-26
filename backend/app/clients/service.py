from psycopg2.errors import UniqueViolation

from app.clients.repository import ClientRepository


class ClientService:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def create_client(self, payload: dict) -> dict:
        try:
            return self.repo.create(payload)
        except UniqueViolation:
            # паспорт уникальный — если уже есть, выдаём понятную ошибку выше в API
            raise ValueError("Клиент с таким паспортом уже существует")

    def get_client(self, client_id: int) -> dict | None:
        return self.repo.get_by_id(client_id)
