from datetime import datetime
from pydantic import BaseModel, Field


class ApplicationCreateRequest(BaseModel):
    client_id: int = Field(gt=0)
    requested_amount: float = Field(gt=0, le=5_000_000)  # диапазоны можно вынести в конфиг
    term_months: int = Field(ge=1, le=84)
    purpose: str = Field(min_length=3, max_length=255)


class ApplicationResponse(BaseModel):
    id: int
    client_id: int
    submitted_at: datetime
    requested_amount: float
    term_months: int
    purpose: str
    status: str
    status_changed_at: datetime
    interest_rate: float | None = None
    comment: str | None = None
