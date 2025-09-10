from uuid import UUID
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .invoice_schema import InvoiceOut


# -------------------
# Base Schema (shared fields)
# -------------------
class SaleBase(BaseModel):
    sale_no: Optional[str] = None  # auto-generated
    gross_value: float = 0
    discount_value: float = 0
    net_value: float = 0
    remarks: Optional[str] = None


# -------------------
# Create Schema (request body)
# -------------------
class SaleCreate(BaseModel):
    appointment_id: UUID  # Only appointment_id is required
    item_type: str  # "product", "service", "package"
    item_id: UUID  # which product/service/package
    discount_id: Optional[UUID] = None  # applied offer/discount (optional)
    remarks: Optional[str] = None


# -------------------
# Update Schema
# -------------------
class SaleUpdate(BaseModel):
    gross_value: Optional[float] = None
    discount_value: Optional[float] = None
    net_value: Optional[float] = None
    remarks: Optional[str] = None


# -------------------
# Response Schemas
# -------------------
class SaleOut(BaseModel):
    id: UUID
    appointment_id: UUID
    gross_value: float
    discount_value: float
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


