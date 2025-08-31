from pydantic import BaseModel
from typing import Optional
import uuid


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
