# schemas/service_schema.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ServiceBase(BaseModel):
    name: str
    description: Optional[str]
    duration: int
    price: float
    category: Optional[str]

class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    id: UUID

    class Config:
        orm_mode = True
