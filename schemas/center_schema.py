# schemas/center_schema.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CenterBase(BaseModel):
    name: str
    address: Optional[str]
    city: Optional[str]
    phone: Optional[str]

class CenterCreate(CenterBase):
    pass

class CenterRead(CenterBase):
    id: UUID

    class Config:
        orm_mode = True
