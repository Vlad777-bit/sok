from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class ClientCreateRequest(BaseModel):
    full_name: str = Field(min_length=3, max_length=255)
    date_of_birth: date

    passport_series: str = Field(min_length=4, max_length=4)
    passport_number: str = Field(min_length=6, max_length=6)

    address_registration: str = Field(min_length=5, max_length=500)
    phone: str = Field(min_length=5, max_length=32)
    email: EmailStr

    workplace: str = Field(min_length=2, max_length=255)
    position: str = Field(min_length=2, max_length=255)
    monthly_income: float = Field(gt=0)

    @field_validator("passport_series")
    @classmethod
    def validate_series(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}", v):
            raise ValueError("passport_series должен быть из 4 цифр")
        return v

    @field_validator("passport_number")
    @classmethod
    def validate_number(cls, v: str) -> str:
        if not re.fullmatch(r"\d{6}", v):
            raise ValueError("passport_number должен быть из 6 цифр")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # очень базово: цифры, +, -, пробелы
        if not re.fullmatch(r"[0-9+\-\s()]{5,32}", v):
            raise ValueError("phone имеет некорректный формат")
        return v


class ClientResponse(BaseModel):
    id: int
    full_name: str
    date_of_birth: date
    passport_series: str
    passport_number: str
    address_registration: str
    phone: str
    email: str
    workplace: str
    position: str
    monthly_income: float
    registered_at: datetime
