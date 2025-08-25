# schemas/provider_schema.py
from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class ProviderBase(BaseModel):
    first_name: str
    last_name: str
    specialization: Optional[str]
    email: EmailStr
    phone: Optional[str]
    center_id: UUID

class ProviderCreate(ProviderBase):
    pass

class ProviderRead(ProviderBase):
    id: UUID

    class Config:
        orm_mode = True
