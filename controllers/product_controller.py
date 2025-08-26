from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from services import product_service
import uuid
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return product_service.get_all_products(db)


@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: uuid.UUID, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = product_service.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated
@router.delete("/{product_id}")
def delete_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted = product_service.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}