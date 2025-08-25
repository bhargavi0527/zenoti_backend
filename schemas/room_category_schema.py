from pydantic import BaseModel
from typing import Optional
from uuid import UUID


# Shared fields
class RoomCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


# Create schema
class RoomCategoryCreate(RoomCategoryBase):
    pass


# Update schema (all fields optional)
class RoomCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# Response schema
class RoomCategoryOut(RoomCategoryBase):
    id: UUID

    class Config:
        from_attributes = True
