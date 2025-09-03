import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String, Date, DateTime, Float, func, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    invoice_no = Column(String, unique=True, nullable=False)
    receipt_no = Column(String, nullable=True)
    payment_no = Column(String, nullable=True)
    zone = Column(String, nullable=True)
    center_code = Column(String, nullable=True)
    center = Column(String, nullable=True)
    invoice_center_code = Column(String, nullable=True)
    invoice_center = Column(String, nullable=True)
    invoice_date = Column(Date, nullable=True)
    invoice_date_full = Column(DateTime, nullable=True)
    total_collection = Column(Float, default=0)
    gross_invoice_value = Column(Float, default=0)
    invoice_discount = Column(Float, default=0)
    net_invoice_value = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"))
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"))
    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"))

    # Relationships
    sale = relationship("Sale", back_populates="invoice", uselist=False)
    guest = relationship("Guest", back_populates="invoices")
    employee = relationship("Employee")
    collections = relationship("Collection", back_populates="invoice", cascade="all, delete-orphan")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("InvoicePayment", back_populates="invoice", cascade="all, delete-orphan")
