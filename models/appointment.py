from sqlalchemy import Column, String, DateTime, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid
from datetime import datetime


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)
    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"), nullable=False)

    status = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    scheduled_time = Column(DateTime, nullable=False)
    appointment_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    center = relationship("Center", back_populates="appointments")
    guest = relationship("Guest", back_populates="appointments")
    provider = relationship("Provider", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    sale = relationship("Sale", back_populates="appointment", uselist=False)
