from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid


class Sale(Base):
    __tablename__ = "sales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    sale_no = Column(String, unique=True, nullable=False)
    sale_date = Column(DateTime(timezone=True), server_default=func.now())
    gross_value = Column(Float, default=0)
    discount_value = Column(Float, default=0)
    net_value = Column(Float, default=0)
    remarks = Column(String, nullable=True)

    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"))
    appointment = relationship("Appointment", back_populates="sale")
    invoice = relationship("Invoice", back_populates="sale", uselist=False)
    collections = relationship("Collection", back_populates="sale", cascade="all, delete-orphan")
