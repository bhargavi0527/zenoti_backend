from pydantic import BaseModel
from typing import Optional
import uuid


class InvoiceItemBase(BaseModel):
    item_type: Optional[str] = None
    item_code: Optional[str] = None
    item_name: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    business_unit: Optional[str] = None
    item_quantity: Optional[int] = 1
    unit_price: Optional[float] = 0
    item_discount: Optional[float] = 0
    net_price: Optional[float] = 0


class InvoiceItemCreate(InvoiceItemBase):
    invoice_id: uuid.UUID


class InvoiceItemUpdate(InvoiceItemBase):
    pass


class InvoiceItemOut(InvoiceItemBase):
    id: uuid.UUID
    invoice_id: uuid.UUID

    class Config:
        orm_mode = True
