from sqlalchemy import Column, String, Boolean, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base
import uuid
from datetime import datetime


class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    employee_code = Column(String, unique=True, nullable=False)   # "100208"
    name = Column(String, nullable=False)                        # "Dr Preethi Havanur"
    job_code = Column(String, nullable=True)                     # "D07"
    designation = Column(String, nullable=True)                  # Doctor, Therapist, Manager
    department = Column(String, nullable=True)                   # Skin, Hair, etc.

    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    center_code = Column(String, nullable=True)                  # HRBR, BLR, etc.
    zone = Column(String, nullable=True)                         # Karnataka, etc.

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
