from fastapi import APIRouter, Depends, HTTPException

from app.applications.models import (
    ApplicationCreateRequest,
    ApplicationResponse,
    ApplicationStatus,
    ApplicationUpdateRequest,
)
from app.applications.repository import ApplicationRepository
from app.applications.service import ApplicationService
from app.audit.repository import AuditRepository
from app.audit.service import AuditService
from app.auth.deps import require_employee
from app.clients.repository import ClientRepository
from app.clients.service import ClientService

router = APIRouter(prefix="/applications", tags=["applications"])

client_service = ClientService(ClientRepository())
service = ApplicationService(ApplicationRepository(), client_service)
audit = AuditService(AuditRepository())


@router.post("", response_model=ApplicationResponse, status_code=201)
def create_application(body: ApplicationCreateRequest):
    try:
        row = service.create_application(body.model_dump())

        # meta — только “безопасные” поля, без ПДн
        audit.log(
            action="APPLICATION_CREATE",
            entity="application",
            entity_id=row["id"],
            actor=None,
            meta={
                "source": "public_webui",
                "requested_amount": float(row["requested_amount"]),
                "term_months": int(row["term_months"]),
                "status": row["status"],
                "interest_rate": float(row["interest_rate"]) if row["interest_rate"] is not None else None,
            },
        )
        return row
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int):
    row = service.get_application(app_id)
    if not row:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    audit.log(action="APPLICATION_READ", entity="application", entity_id=app_id, actor=None)
    return row


@router.get("", response_model=list[ApplicationResponse], dependencies=[Depends(require_employee)])
def list_applications(
        limit: int = 20,
        offset: int = 0,
        status: ApplicationStatus | None = None,
        current_user: dict = Depends(require_employee),
):
    audit.log(
        action="APPLICATION_LIST",
        entity="application",
        entity_id=None,
        actor=current_user,
        meta={"limit": limit, "offset": offset, "status": status.value if status else None},
    )
    return service.list_applications(limit=limit, offset=offset, status=status.value if status else None)


@router.patch("/{app_id}", response_model=ApplicationResponse)
def patch_application(
        app_id: int,
        body: ApplicationUpdateRequest,
        current_user: dict = Depends(require_employee),
):
    try:
        patch = body.model_dump(exclude_none=True)

        # Pydantic может дать Enum-объект — приводим к строке
        if "status" in patch and hasattr(patch["status"], "value"):
            patch["status"] = patch["status"].value

        old_row, new_row = service.update_application(app_id, patch)

        audit.log(
            action="APPLICATION_UPDATE",
            entity="application",
            entity_id=app_id,
            actor=current_user,
            meta={
                "old_status": old_row["status"],
                "new_status": new_row["status"],
            },
        )
        return new_row
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
