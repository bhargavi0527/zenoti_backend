from pydantic import BaseModel
from typing import Optional
from uuid import UUID


# Shared fields
class RoomBase(BaseModel):
    code: str
    name: str
    room_category_id: UUID
    description: Optional[str] = None
    capacity: int = 1
    only_one_appointment: bool = False
    can_exceed_capacity: bool = False
    center_id: UUID
    is_active: bool = True
    dq_check_remark: Optional[str] = None


# Create schema
class RoomCreate(RoomBase):
    pass


# Update schema (all fields optional)
class RoomUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    room_category_id: Optional[UUID] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    only_one_appointment: Optional[bool] = None
    can_exceed_capacity: Optional[bool] = None
    center_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    dq_check_remark: Optional[str] = None


# Response schema
class RoomOut(RoomBase):
    id: UUID

    class Config:
        from_attributes = True
