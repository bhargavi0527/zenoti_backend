from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid


class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    collection_no = Column(String, unique=True, nullable=False)
    payment_method = Column(String, nullable=False)
    amount = Column(Float, default=0)
    transaction_no = Column(String, nullable=True)
    reference_no = Column(String, nullable=True)
    remarks = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"))
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"))
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"))

    # Relationships
    sale = relationship("Sale", back_populates="collections")
    employee = relationship("Employee")
    invoice = relationship("Invoice", back_populates="collections")
