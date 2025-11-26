from fastapi import APIRouter, HTTPException

from app.clients.models import ClientCreateRequest, ClientResponse
from app.clients.repository import ClientRepository
from app.clients.service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])

service = ClientService(ClientRepository())


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(body: ClientCreateRequest):
    try:
        row = service.create_client(body.model_dump())
        return row
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int):
    row = service.get_client(client_id)
    if not row:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return row
