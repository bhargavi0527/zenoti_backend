# models/offer_discount.py
import uuid


from sqlalchemy import Column, String, Float, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.db import Base
import enum
from datetime import datetime


class DiscountType(str, enum.Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class OfferDiscount(Base):
    __tablename__ = "offers_discounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_type = Column(String)  # 'service', 'product', 'package'
    item_id = Column(UUID(as_uuid=True))  # reference to service/product/package
    discount_type = Column(Enum(DiscountType), default=DiscountType.FIXED)
    discount_value = Column(Float, default=0)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    sales = relationship("Sale", back_populates="offer_discount")
