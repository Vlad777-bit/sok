from fastapi import APIRouter, HTTPException, Depends

from app.auth.deps import require_employee
from app.audit.repository import AuditRepository
from app.audit.service import AuditService
from app.clients.models import ClientCreateRequest, ClientResponse
from app.clients.repository import ClientRepository
from app.clients.service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])

service = ClientService(ClientRepository())
audit = AuditService(AuditRepository())


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(body: ClientCreateRequest):
    try:
        row = service.create_client(body.model_dump())

        # В meta кладём только “техническое/безопасное” (без паспорта/телефона/email).
        audit.log(
            action="CLIENT_CREATE",
            entity="client",
            entity_id=row["id"],
            actor=None,
            meta={"source": "public_webui"}
        )
        return row
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int):
    row = service.get_client(client_id)
    if not row:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    # логируем факт чтения (без ПДн)
    audit.log(action="CLIENT_READ", entity="client", entity_id=client_id, actor=None)
    return row


@router.get("", response_model=list[ClientResponse])
def list_clients(
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(require_employee),
):
    audit.log(action="CLIENT_LIST", entity="client", entity_id=None, actor=current_user, meta={"limit": limit, "offset": offset})
    return service.list_clients(limit=limit, offset=offset)
