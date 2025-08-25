from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database.db import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    specialization = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)

    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=False)
