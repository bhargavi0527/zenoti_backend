from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models import Invoice
from services import invoice_service
from schemas.invoice_schema import InvoiceCreate, InvoiceUpdate, InvoiceOut
from typing import List
import uuid

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceOut)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    return invoice_service.create_invoice(db, invoice)


@router.get("/", response_model=List[InvoiceOut])
def get_all_invoices(db: Session = Depends(get_db)):
    return invoice_service.get_invoices(db)


@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    invoice = invoice_service.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.put("/{invoice_id}", response_model=InvoiceOut)
def update_invoice(invoice_id: uuid.UUID, invoice: InvoiceUpdate, db: Session = Depends(get_db)):
    updated = invoice_service.update_invoice(db, invoice_id, invoice)
    if not updated:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return updated


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted = invoice_service.delete_invoice(db, invoice_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted"}


@router.get("/guest/{guest_id}/ids", response_model=list[str])
def get_invoice_ids_by_guest(guest_id: str, db: Session = Depends(get_db)):
    invoices = db.query(Invoice.id).filter(Invoice.guest_id == guest_id).all()

    # return empty list if none
    return [str(inv[0]) for inv in invoices]