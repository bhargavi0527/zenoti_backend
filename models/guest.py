import uuid
from datetime import date, datetime
from sqlalchemy import Column, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base

def generate_guest_code():
    return f"GUEST{str(uuid.uuid4().int)[:6]}"

class Guest(Base):
    __tablename__ = "guests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    guest_code = Column(String, nullable=False, unique=True, index=True, default=generate_guest_code)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=False)

    center_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone_no = Column(String, nullable=False)
    home_no = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    is_minor = Column(Boolean, default=False)
    nationality = Column(String, nullable=True)
    language = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    center = relationship("Center", back_populates="guests")
    appointments = relationship("Appointment", back_populates="guest")
    invoices = relationship("Invoice", back_populates="guest")
