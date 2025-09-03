from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.db import Base
import uuid
from datetime import datetime


class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    employee_code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    job_code = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    department = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    center_code = Column(String, nullable=True)
    zone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
