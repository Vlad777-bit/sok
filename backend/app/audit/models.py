from datetime import datetime
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: int
    created_at: datetime
    actor_user_id: int | None = None
    actor_username: str | None = None
    actor_role: str | None = None
    action: str
    entity: str
    entity_id: int | None = None
    meta: dict
