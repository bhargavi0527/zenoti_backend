from datetime import datetime


from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid

def generate_sale_no():
    # Example: SALE-<8 random hex digits>
    return f"SALE-{uuid.uuid4().hex[:4]}"

class Sale(Base):
    __tablename__ = "sales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    sale_no = Column(String, unique=True, nullable=False, default=generate_sale_no)

    gross_value = Column(Float, default=0)
    discount_value = Column(Float, default=0)
    net_value = Column(Float, default=0)
    remarks = Column(String, nullable=True)
    sale_date = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)

    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"), nullable=False)
    appointment = relationship("Appointment", back_populates="sale", uselist=False)

    # ⬇️ Payments now belong directly to Sale
    payments = relationship("InvoicePayment", back_populates="sale", cascade="all, delete-orphan")

    # ⬇️ Invoice is generated later from Sale + Payments
    invoice = relationship("Invoice", back_populates="sale", uselist=False)

    collections = relationship("Collection", back_populates="sale", cascade="all, delete-orphan")

    discount_id = Column(UUID(as_uuid=True), ForeignKey("offers_discounts.id"), nullable=True)
    offer_discount = relationship("OfferDiscount")