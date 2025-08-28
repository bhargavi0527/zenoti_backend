# schemas/guest_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import date, datetime


class GuestBase(BaseModel):
    center_id: Optional[str] = None  # Optional
    center_name: Optional[str] = None  # Optional

    username: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    phone_no: str
    home_no: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_minor: Optional[bool] = False
    nationality: Optional[str] = None
    language: Optional[str] = None


class GuestCreate(GuestBase):
    pass


class GuestResponse(GuestBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
