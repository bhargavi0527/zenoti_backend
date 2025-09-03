import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models import Invoice
from schemas.invoice_schema import InvoiceOut
from schemas.sales_schema import (
    SaleCreate, SaleUpdate, SaleResponse
)
from services import sales_service
from typing import List


router = APIRouter(prefix="/sales", tags=["Sales"])


# -------------------
# Sale Endpoints
# -------------------
@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    return sales_service.create_sale(db, sale)


@router.get("/", response_model=List[SaleResponse])
def list_sales(db: Session = Depends(get_db)):
    return sales_service.get_sales(db)


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: str, db: Session = Depends(get_db)):
    sale = sales_service.get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: str, sale: SaleUpdate, db: Session = Depends(get_db)):
    updated = sales_service.update_sale(db, sale_id, sale)
    if not updated:
        raise HTTPException(status_code=404, detail="Sale not found")
    return updated


@router.delete("/{sale_id}")
def delete_sale(sale_id: str, db: Session = Depends(get_db)):
    deleted = sales_service.delete_sale(db, sale_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"detail": "Sale deleted successfully"}


@router.get("/{sale_id}/invoice", response_model=InvoiceOut)
def get_invoice_for_sale(sale_id: uuid.UUID, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.sale_id == sale_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found for this sale")
    return invoice