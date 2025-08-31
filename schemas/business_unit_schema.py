from pydantic import BaseModel
from typing import Optional
import uuid


class BusinessUnitBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class BusinessUnitCreate(BusinessUnitBase):
    pass


class BusinessUnitUpdate(BusinessUnitBase):
    pass


class BusinessUnitResponse(BusinessUnitBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
