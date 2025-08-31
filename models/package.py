import uuid
from sqlalchemy import Column, String, Text, Boolean, Date, Integer, DECIMAL, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)

    # Foreign Keys
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    business_unit_id = Column(UUID(as_uuid=True), ForeignKey("business_unit.id"), nullable=True)
    version_id = Column(UUID(as_uuid=True), nullable=True)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=True)

    # Other fields
    time = Column(Integer, nullable=True)
    booking_start_date = Column(Date, nullable=True)
    booking_end_date = Column(Date, nullable=True)

    commission_eligible = Column(Boolean, default=False)
    commission_factor = Column(DECIMAL(5, 2), nullable=True)
    commission_type = Column(String(50), nullable=True)
    commission_value = Column(DECIMAL(10, 2), nullable=True)

    series_package_type = Column(String(100), nullable=True)
    series_package_cost_to_center = Column(DECIMAL(12, 2), nullable=True)

    tags = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)
    dq_check_remark = Column(Text, nullable=True)

    # Relationships
    business_unit = relationship("BusinessUnit", back_populates="packages")
    category = relationship("Category", back_populates="packages")
    center = relationship("Center", backref="packages", lazy="joined")
