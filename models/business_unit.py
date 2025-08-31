import uuid
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base


class BusinessUnit(Base):
    __tablename__ = "business_unit"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    # One-to-many relationship with Package
    packages = relationship("Package", back_populates="business_unit")
