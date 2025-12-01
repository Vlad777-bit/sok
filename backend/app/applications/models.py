from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    NEW = "NEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ApplicationCreateRequest(BaseModel):
    client_id: int = Field(gt=0)
    requested_amount: float = Field(gt=0, le=5_000_000)
    term_months: int = Field(ge=1, le=84)
    purpose: str = Field(min_length=3, max_length=255)


class ApplicationUpdateRequest(BaseModel):
    status: ApplicationStatus | None = None
    interest_rate: float | None = Field(default=None, ge=0, le=99.99)
    comment: str | None = Field(default=None, max_length=500)


class ApplicationResponse(BaseModel):
    id: int
    client_id: int
    submitted_at: datetime
    requested_amount: float
    term_months: int
    purpose: str
    status: ApplicationStatus
    status_changed_at: datetime
    interest_rate: float | None = None
    comment: str | None = None
