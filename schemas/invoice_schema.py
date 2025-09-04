from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class InvoiceBase(BaseModel):
    receipt_no: Optional[str] = None
    payment_no: Optional[str] = None
    zone: Optional[str] = None
    center_code: Optional[str] = None
    center: Optional[str] = None
    invoice_center_code: Optional[str] = None
    invoice_center: Optional[str] = None
    invoice_date: Optional[date] = None
    invoice_date_full: Optional[datetime] = None
    total_collection: float = 0
    gross_invoice_value: float = 0
    invoice_discount: float = 0
    net_invoice_value: float = 0


class InvoiceCreate(InvoiceBase):
    sale_id: UUID
    guest_id: UUID
    employee_id: Optional[UUID] = None
    invoice_no: Optional[str] = None  # system can auto-generate


class InvoiceUpdate(InvoiceBase):
    invoice_no: Optional[str] = None
    guest_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    sale_id: Optional[UUID] = None


class InvoiceOut(InvoiceBase):
    id: UUID
    invoice_no: str
    sale_id: Optional[UUID] = None

    guest_id: UUID
    employee_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
