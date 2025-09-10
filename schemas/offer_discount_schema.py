# schemas/offer_discount_schema.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from enum import Enum
from datetime import datetime

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class OfferDiscountBase(BaseModel):
    item_type: str  # 'service', 'product', 'package'
    item_id: UUID
    discount_type: DiscountType
    discount_value: float
    description: Optional[str] = None

class OfferDiscountCreate(OfferDiscountBase):
    pass

class OfferDiscountUpdate(BaseModel):
    discount_type: Optional[DiscountType] = None
    discount_value: Optional[float] = None
    description: Optional[str] = None

class OfferDiscountResponse(OfferDiscountBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

