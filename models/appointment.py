# models/appointment.py
from sqlalchemy import Column, String, DateTime, Date, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid
from datetime import datetime


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    center_id = Column(UUID(as_uuid=True), nullable=False)
    provider_id = Column(UUID(as_uuid=True), nullable=False)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String, nullable=False)
    notes = Column(Text, nullable=True)

    # ✅ both datetime & date
    scheduled_time = Column(DateTime, nullable=False)
    appointment_date = Column(Date, nullable=False)

    guest_id = Column(UUID(as_uuid=True), ForeignKey("guests.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


