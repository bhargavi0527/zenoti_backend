from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import relationship

from database.db import Base
def generate_service_code():
    # Example: "SERV" + 4 random digits
    return f"SERV{str(uuid.uuid4().int)[:4]}"
class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    service_code = Column(String, nullable=False, unique=True, index=True, default=generate_service_code)  # ✅ new
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=False)  # in minutes
    price = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    appointments = relationship("Appointment", back_populates="service")
