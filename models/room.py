from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database.db import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    room_category_id = Column(UUID(as_uuid=True), ForeignKey("room_categories.id"), nullable=False)
    description = Column(String(255))
    capacity = Column(Integer, nullable=False, default=1)
    only_one_appointment = Column(Boolean, default=False)
    can_exceed_capacity = Column(Boolean, default=False)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"))
    is_active = Column(Boolean, default=True)
    dq_check_remark = Column(String(255))

    # Relationship to RoomCategory
    category = relationship("RoomCategory", back_populates="rooms")
