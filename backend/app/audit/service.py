from app.audit.repository import AuditRepository


class AuditService:
    def __init__(self, repo: AuditRepository):
        self.repo = repo

    def log(self, action: str, entity: str, entity_id: int | None, actor: dict | None, meta: dict | None = None):
        self.repo.add(action=action, entity=entity, entity_id=entity_id, actor=actor, meta=meta)
