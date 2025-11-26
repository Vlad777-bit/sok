from app.applications.repository import ApplicationRepository
from app.clients.service import ClientService


class ApplicationService:
    def __init__(self, repo: ApplicationRepository, client_service: ClientService):
        self.repo = repo
        self.client_service = client_service

    def _make_decision(self, monthly_income: float, requested_amount: float, term_months: int) -> tuple[str, float | None, str]:
        """
        Упрощённый скоринг:
        - считаем примерный ежемесячный платёж = (сумма / срок) * 1.2 (условно "проценты")
        - одобряем, если платёж <= 40% дохода
        """
        estimated_payment = (requested_amount / term_months) * 1.2
        limit = monthly_income * 0.4

        if estimated_payment <= limit:
            rate = 19.9
            comment = f"Одобрено: платёж ~{estimated_payment:.2f} <= лимита {limit:.2f}"
            return "APPROVED", rate, comment

        comment = f"Отклонено: платёж ~{estimated_payment:.2f} > лимита {limit:.2f}"
        return "REJECTED", None, comment

    def create_application(self, payload: dict) -> dict:
        client_id = payload["client_id"]
        client = self.client_service.get_client(client_id)
        if not client:
            raise ValueError("Клиент не найден")

        status, rate, comment = self._make_decision(
            monthly_income=float(client["monthly_income"]),
            requested_amount=float(payload["requested_amount"]),
            term_months=int(payload["term_months"]),
        )

        data = {**payload, "status": status, "interest_rate": rate, "comment": comment}
        return self.repo.create(data)

    def get_application(self, app_id: int) -> dict | None:
        return self.repo.get_by_id(app_id)

    def list_applications(self, limit: int, offset: int, status: str | None) -> list[dict]:
        return self.repo.list(limit=limit, offset=offset, status=status)
