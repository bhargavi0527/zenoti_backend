from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    code = Column(String, nullable=False, unique=True)        # Product Code
    name = Column(String, nullable=False)                     # Product Name
    color = Column(String, nullable=True)                     # Product Color
    size = Column(String, nullable=True)                      # Product Size
    brand = Column(String, nullable=True)                     # Brand Name
    category = Column(String, nullable=True)                  # Category (e.g., Clothing)
    subcategory = Column(String, nullable=True)               # Subcategory (e.g., Shirts)
    business_unit = Column(String, nullable=True)             # Business unit (e.g., Retail, Wholesale)
    type = Column(String, nullable=True)                      # Type (e.g., Regular, Seasonal)
    sale_price = Column(Float, nullable=False, default=0.0)   # Sale price (₹)
    mrp = Column(Float, nullable=False, default=0.0)          # MRP (₹)
    amount = Column(Integer, nullable=False, default=0)       # Stock Quantity
    in_use = Column(Boolean, default=True)                    # Whether product is active
    status = Column(String, default="Available")              # Product status (Available/Out of Stock/Discontinued)
