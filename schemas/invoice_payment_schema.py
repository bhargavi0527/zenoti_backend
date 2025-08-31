from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


# ✅ Base schema (shared fields)
class InvoicePaymentBase(BaseModel):
    payment_method: str   # e.g., "cash", "card", "upi", "wallet"
    amount: float
    reference_no: Optional[str] = None  # transaction id / cheque no / UPI ref
    remarks: Optional[str] = None


# ✅ Create schema (extra: invoice_id required)
class InvoicePaymentCreate(InvoicePaymentBase):
    invoice_id: uuid.UUID


# ✅ Update schema (all optional fields for PATCH/PUT)
class InvoicePaymentUpdate(BaseModel):
    payment_method: Optional[str] = None
    amount: Optional[float] = None
    reference_no: Optional[str] = None
    remarks: Optional[str] = None


# ✅ Response schema (ORM mode enabled)
class InvoicePaymentOut(InvoicePaymentBase):
    id: uuid.UUID
    invoice_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
