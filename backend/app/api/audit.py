from fastapi import APIRouter, Depends

from app.audit.models import AuditLogResponse
from app.audit.repository import AuditRepository
from app.auth.deps import require_admin

router = APIRouter(prefix="/audit", tags=["audit"])

repo = AuditRepository()


@router.get("", response_model=list[AuditLogResponse])
def list_audit(limit: int = 50, current_user: dict = Depends(require_admin)):
    # ADMIN может посмотреть последние события
    return repo.list_latest(limit=limit)
