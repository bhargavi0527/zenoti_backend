from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .invoice_schema import InvoiceOut


class SaleBase(BaseModel):
    sale_no: Optional[str] = None  # can auto-generate
    gross_value: float = 0
    discount_value: float = 0
    net_value: float = 0
    remarks: Optional[str] = None


class SaleCreate(BaseModel):
    appointment_id: UUID  # appointment must exist
    remarks: Optional[str] = None


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

    class Config:
        from_attributes = True


class SaleResponse(SaleBase):
    id: UUID
    sale_date: datetime
    appointment_id: Optional[UUID] = None
    invoice: Optional[InvoiceOut] = None  # include related invoice

    class Config:
        from_attributes = True
