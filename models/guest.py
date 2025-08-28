# models/guest.py
import uuid
from datetime import date, datetime
from sqlalchemy import Column, String, Boolean, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base

def generate_guest_code():
    # Example: GUEST + 6 random digits
    return f"GUEST{str(uuid.uuid4().int)[:6]}"
class Guest(Base):
    __tablename__ = "guests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    guest_code = Column(String, nullable=False, unique=True, index=True, default=generate_guest_code)

    center_id = Column(String, nullable=False)
    center_name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)

    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)

    email = Column(String, nullable=False, unique=True, index=True)
    phone_no = Column(String, nullable=False)
    home_no = Column(String, nullable=True)

    gender = Column(String, nullable=True)  # could be 'Male', 'Female', 'Other'
    date_of_birth = Column(Date, nullable=True)
    is_minor = Column(Boolean, default=False)

    nationality = Column(String, nullable=True)
    language = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
