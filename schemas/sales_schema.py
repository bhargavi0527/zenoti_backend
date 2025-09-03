from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


# -------------------
# Invoice Schema (minimal for nesting inside Sale)
# -------------------
class InvoiceOut(BaseModel):
    id: UUID
    invoice_no: str
    amount_due: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


# -------------------
# Sale Schemas
# -------------------
class SaleBase(BaseModel):
    sale_no: str
    gross_value: float = 0
    discount_value: float = 0
    net_value: float = 0
    remarks: Optional[str] = None


class SaleCreate(SaleBase):
    appointment_id: Optional[UUID] = None


class SaleUpdate(BaseModel):
    gross_value: Optional[float] = None
    discount_value: Optional[float] = None
    net_value: Optional[float] = None
    remarks: Optional[str] = None


class SaleOut(BaseModel):
    id: UUID
    appointment_id: UUID
    net_value: float
    created_at: datetime


class SaleResponse(SaleBase):
    id: uuid.UUID
    sale_date: datetime
    appointment_id: Optional[UUID] = None
    invoice: Optional[InvoiceOut] = None   # 🔹 include related invoice

    class Config:
        orm_mode = True
