from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    item_type = Column(String, nullable=True)   # e.g. Service/Product
    item_code = Column(String, nullable=True)
    item_name = Column(String, nullable=True)
    item_tags = Column(String, nullable=True)
    business_unit = Column(String, nullable=True)
    category = Column(String, nullable=True)
    sub_category = Column(String, nullable=True)

    item_quantity = Column(Integer, default=1)
    unit_price = Column(Float, default=0)
    item_discount = Column(Float, default=0)
    net_price = Column(Float, default=0)

    row_num = Column(Integer, nullable=True)
    item_row_num = Column(Integer, nullable=True)

    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"))
    invoice = relationship("Invoice", back_populates="items")
