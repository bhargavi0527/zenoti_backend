from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid


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

    cash = Column(Float, default=0)
    card = Column(Float, default=0)
    check = Column(Float, default=0)
    custom = Column(Float, default=0)
    lp = Column(Float, default=0)
    gift_card = Column(Float, default=0)
    prepaid_card = Column(Float, default=0)

    # Relations
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"))
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"))

    guest = relationship("Guest")
    employee = relationship("Employee")
    items = relationship("InvoiceItem", back_populates="invoice")
