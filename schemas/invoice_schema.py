from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


class InvoiceBase(BaseModel):
    invoice_number: str
    customer_name: str
    customer_contact: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: float
    discount: Optional[float] = 0
    net_amount: float
    status: str = "PENDING"


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_contact: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: Optional[float] = None
    discount: Optional[float] = None
    net_amount: Optional[float] = None
    status: Optional[str] = None


class InvoiceOut(InvoiceBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        orm_mode = True
