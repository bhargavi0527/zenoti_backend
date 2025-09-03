from uuid import UUID

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class CollectionBase(BaseModel):
    collection_no: str
    payment_method: str
    amount: float
    transaction_no: Optional[str] = None
    reference_no: Optional[str] = None
    remarks: Optional[str] = None


class CollectionCreate(CollectionBase):
    invoice_id: UUID
    payment_method: str
    amount: float


class CollectionUpdate(BaseModel):
    payment_method: Optional[str] = None
    amount: Optional[float] = None
    transaction_no: Optional[str] = None
    reference_no: Optional[str] = None
    remarks: Optional[str] = None

class CollectionOut(BaseModel):
    id: UUID
    invoice_id: UUID
    payment_method: str
    amount: float
    created_at: datetime

class CollectionResponse(CollectionBase):
    id: uuid.UUID
    created_at: datetime
    sale_id: uuid.UUID
    employee_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
