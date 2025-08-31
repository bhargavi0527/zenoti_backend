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


class ServiceUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    duration: Optional[int]
    price: Optional[float]
    category: Optional[str]


class ServiceRead(ServiceBase):
    id: UUID
    service_code: str   # include the auto-generated service_code

    class Config:
        orm_mode = True
