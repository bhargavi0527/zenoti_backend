from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models import Invoice, Appointment, Guest, Collection
from schemas.collection_schema import CollectionResponse
from services import invoice_service
from schemas.invoice_schema import InvoiceCreate, InvoiceUpdate, InvoiceOut
from typing import List
import uuid
from datetime import datetime   # ✅ added

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


@router.post("/get-or-create/{guest_id}")
def get_or_create_invoice_for_guest(guest_id: uuid.UUID, db: Session = Depends(get_db)):
    # 🔹 Check if guest exists
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    # 🔹 Try to get existing invoice for this guest
    invoice = db.query(Invoice).filter(Invoice.guest_id == guest_id).first()

    if invoice:
        return {
            "message": "Invoice already exists",
            "invoice_id": str(invoice.id),
            "invoice_no": invoice.invoice_no,
        }

    # 🔹 If not, create a new invoice
    new_invoice = Invoice(
        invoice_no=f"INV-{uuid.uuid4().hex[:8]}",
        guest_id=guest_id,
        gross_invoice_value=0,
        net_invoice_value=0,
        total_collection=0,
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return {
        "message": "New invoice created",
        "invoice_id": str(new_invoice.id),
        "invoice_no": new_invoice.invoice_no,
    }


@router.get("/{invoice_id}/collections", response_model=list[CollectionResponse])
def get_collections_for_invoice(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    # 🔹 Retrieve all collections for the given invoice_id
    collections = db.query(Collection).filter(Collection.invoice_id == invoice_id).all()

    # 🔹 Explicitly convert each Collection object to a CollectionResponse Pydantic model
    return [
        CollectionResponse.from_orm(collection) for collection in collections
    ]