from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database.db import Base

class Center(Base):
    __tablename__ = "centers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    # New fields
    code = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=True)  # human readable name
    country = Column(String, nullable=True)
    state = Column(String, nullable=True)
    contact_info_phone = Column(String, nullable=True)
    contact_info_email = Column(String, nullable=True)