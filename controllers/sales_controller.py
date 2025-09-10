from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.sales_schema import SaleCreate, SaleUpdate, SaleResponse, SaleOut
from services import sales_service
import uuid

router = APIRouter(prefix="/sales", tags=["Sales"])


# -------------------
# Create Sale
# -------------------
@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    try:
        created_sale = sales_service.create_sale(db, sale)
        return created_sale
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -------------------
# List all sales
# -------------------
@router.get("/", response_model=list[SaleOut])
def list_sales(db: Session = Depends(get_db)):
    return sales_service.get_sales(db)


# -------------------
# Get single sale
# -------------------
@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: str, db: Session = Depends(get_db)):
    try:
        sale_uuid = uuid.UUID(sale_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid sale_id format")

    sale = sales_service.get_sale(db, sale_uuid)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


# -------------------
# Update Sale
# -------------------
@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: str, sale_data: SaleUpdate, db: Session = Depends(get_db)):
    try:
        sale_uuid = uuid.UUID(sale_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid sale_id format")

    updated_sale = sales_service.update_sale(db, sale_uuid, sale_data)
    if not updated_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return updated_sale


# -------------------
# Delete Sale
# -------------------
@router.delete("/{sale_id}")
def delete_sale(sale_id: str, db: Session = Depends(get_db)):
    try:
        sale_uuid = uuid.UUID(sale_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid sale_id format")

    success = sales_service.delete_sale(db, sale_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"detail": "Sale deleted successfully"}
