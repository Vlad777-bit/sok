from fastapi import APIRouter, HTTPException

from app.applications.models import ApplicationCreateRequest, ApplicationResponse
from app.applications.repository import ApplicationRepository
from app.applications.service import ApplicationService
from app.clients.repository import ClientRepository
from app.clients.service import ClientService

router = APIRouter(prefix="/applications", tags=["applications"])

client_service = ClientService(ClientRepository())
service = ApplicationService(ApplicationRepository(), client_service)


@router.post("", response_model=ApplicationResponse, status_code=201)
def create_application(body: ApplicationCreateRequest):
    try:
        row = service.create_application(body.model_dump())
        return row
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int):
    row = service.get_application(app_id)
    if not row:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return row
