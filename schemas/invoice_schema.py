from pydantic import BaseModel
from typing import Optional, List
import uuid
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

    cash: float = 0
    card: float = 0
    check: float = 0
    custom: float = 0
    lp: float = 0
    gift_card: float = 0
    prepaid_card: float = 0

    guest_id: uuid.UUID
    employee_id: Optional[uuid.UUID] = None


class InvoiceCreate(InvoiceBase):
    pass


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

    cash: Optional[float] = None
    card: Optional[float] = None
    check: Optional[float] = None
    custom: Optional[float] = None
    lp: Optional[float] = None
    gift_card: Optional[float] = None
    prepaid_card: Optional[float] = None

    guest_id: Optional[uuid.UUID] = None
    employee_id: Optional[uuid.UUID] = None


class InvoiceOut(InvoiceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
