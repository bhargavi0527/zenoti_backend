from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime


# ------------------------
# Base Schema
# ------------------------
class InvoicePaymentBase(BaseModel):
    payment_method: str   # e.g., "cash", "card", "upi", "wallet"
    amount: float
    transaction_no: Optional[str] = None  # card/upi ref number, cheque no, etc.
    remarks: Optional[str] = None


# ------------------------
# Create Schema
# ------------------------
class InvoicePaymentCreate(InvoicePaymentBase):
    sale_id: uuid.UUID   # link payment to a sale


# ------------------------
# Update Schema
# ------------------------
class InvoicePaymentUpdate(BaseModel):
    payment_method: Optional[str] = None
    amount: Optional[float] = None
    transaction_no: Optional[str] = None
    remarks: Optional[str] = None


# ------------------------
# Response Schema
# ------------------------
class InvoicePaymentOut(InvoicePaymentBase):
    id: uuid.UUID
    sale_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
