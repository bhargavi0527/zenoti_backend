# schemas/guest_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import date, datetime


class GuestBase(BaseModel):
    center_id: Optional[str] = None
    center_name: Optional[str] = None

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


# ✅ For updating, make all fields optional
class GuestUpdate(BaseModel):
    center_id: Optional[str] = None
    center_name: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_no: Optional[str] = None
    home_no: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_minor: Optional[bool] = None
    nationality: Optional[str] = None
    language: Optional[str] = None


class GuestResponse(GuestBase):
    id: uuid.UUID
    center_id: Optional[uuid.UUID] = None
    guest_code: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
