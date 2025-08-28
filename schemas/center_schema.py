from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class CenterBase(BaseModel):
    code: str
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    display_name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    contact_info_phone: Optional[str] = None
    contact_info_email: Optional[EmailStr] = None

class CenterCreate(CenterBase):
    pass

class CenterRead(CenterBase):
    id: UUID

    class Config:
        orm_mode = True
