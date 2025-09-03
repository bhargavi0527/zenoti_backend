from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid


class Center(Base):
    __tablename__ = "centers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    code = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    contact_info_phone = Column(String, nullable=True)
    contact_info_email = Column(String, nullable=True)

    # Relationships
    guests = relationship("Guest", back_populates="center")
    providers = relationship("Provider", back_populates="center")
    appointments = relationship("Appointment", back_populates="center")
