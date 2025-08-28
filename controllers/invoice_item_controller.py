from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from services import invoice_item_service
from schemas.invoice_item_schema import InvoiceItemCreate, InvoiceItemUpdate, InvoiceItemOut
from typing import List
import uuid

router = APIRouter(prefix="/invoice-items", tags=["Invoice Items"])


@router.post("/", response_model=InvoiceItemOut)
def create_item(item: InvoiceItemCreate, db: Session = Depends(get_db)):
    return invoice_item_service.create_invoice_item(db, item)


@router.get("/invoice/{invoice_id}", response_model=List[InvoiceItemOut])
def get_items(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    return invoice_item_service.get_items_by_invoice(db, invoice_id)


@router.get("/{item_id}", response_model=InvoiceItemOut)
def get_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    item = invoice_item_service.get_invoice_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Invoice Item not found")
    return item


@router.put("/{item_id}", response_model=InvoiceItemOut)
def update_item(item_id: uuid.UUID, item: InvoiceItemUpdate, db: Session = Depends(get_db)):
    updated = invoice_item_service.update_invoice_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice Item not found")
    return updated


@router.delete("/{item_id}")
def delete_item(item_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted = invoice_item_service.delete_invoice_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice Item not found")
    return {"message": "Invoice item deleted"}
