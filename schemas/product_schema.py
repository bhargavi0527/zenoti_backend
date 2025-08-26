from pydantic import BaseModel
from typing import Optional
import uuid


class ProductBase(BaseModel):
    code: str
    name: str
    color: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    business_unit: Optional[str] = None
    type: Optional[str] = None
    sale_price: float
    mrp: float
    amount: int
    in_use: Optional[bool] = True
    status: Optional[str] = "Available"


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    business_unit: Optional[str] = None
    type: Optional[str] = None
    sale_price: Optional[float] = None
    mrp: Optional[float] = None
    amount: Optional[int] = None
    in_use: Optional[bool] = None
    status: Optional[str] = None


class ProductResponse(ProductBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
