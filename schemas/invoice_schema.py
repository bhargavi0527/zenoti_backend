from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvoiceBase(BaseModel):
    invoice_no: str
    receipt_no: Optional[str] = None
    payment_no: Optional[str] = None

    zone: Optional[str] = None
    center_code: Optional[str] = None
    center: Optional[str] = None
    invoice_center_code: Optional[str] = None
    invoice_center: Optional[str] = None

    invoice_date: Optional[datetime] = None
    invoice_date_full: Optional[datetime] = None

    total_collection: float = 0
    gross_invoice_value: float = 0
    invoice_discount: float = 0
    net_invoice_value: float = 0

    guest_id: UUID
    employee_id: Optional[UUID] = None


class InvoiceCreate(InvoiceBase):
    sale_id: UUID



class InvoiceUpdate(BaseModel):
    invoice_no: Optional[str] = None
    receipt_no: Optional[str] = None
    payment_no: Optional[str] = None

    zone: Optional[str] = None
    center_code: Optional[str] = None
    center: Optional[str] = None
    invoice_center_code: Optional[str] = None
    invoice_center: Optional[str] = None

    invoice_date: Optional[datetime] = None
    invoice_date_full: Optional[datetime] = None

    total_collection: Optional[float] = None
    gross_invoice_value: Optional[float] = None
    invoice_discount: Optional[float] = None
    net_invoice_value: Optional[float] = None

    guest_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None


class InvoiceOut(BaseModel):
    id: UUID
    invoice_no: str
    receipt_no: Optional[str] = None
    payment_no: Optional[str] = None
    zone: Optional[str] = None
    center_code: Optional[str] = None
    center: Optional[str] = None
    invoice_center_code: Optional[str] = None
    invoice_center: Optional[str] = None
    invoice_date: Optional[datetime] = None
    invoice_date_full: Optional[datetime] = None
    total_collection: float
    gross_invoice_value: float
    invoice_discount: float
    net_invoice_value: float
    guest_id: UUID
    employee_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
