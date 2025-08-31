# controllers/invoice_payment_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.invoice_payment_schema import InvoicePaymentCreate, InvoicePaymentUpdate, InvoicePaymentOut
from services import invoice_payment_service
import uuid
from typing import List

router = APIRouter(prefix="/payments", tags=["Invoice Payments"])


@router.post("/", response_model=InvoicePaymentOut)
def create_payment(payment: InvoicePaymentCreate, db: Session = Depends(get_db)):
    return invoice_payment_service.create_invoice_payment(db, payment)


@router.get("/{payment_id}", response_model=InvoicePaymentOut)
def get_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    db_payment = invoice_payment_service.get_invoice_payment(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.get("/invoice/{invoice_id}", response_model=List[InvoicePaymentOut])
def list_invoice_payments(invoice_id: uuid.UUID, db: Session = Depends(get_db)):
    return invoice_payment_service.get_payments_by_invoice(db, invoice_id)


@router.put("/{payment_id}", response_model=InvoicePaymentOut)
def update_payment(payment_id: uuid.UUID, payment_update: InvoicePaymentUpdate, db: Session = Depends(get_db)):
    updated_payment = invoice_payment_service.update_invoice_payment(db, payment_id, payment_update)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment


@router.delete("/{payment_id}")
def delete_payment(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    success = invoice_payment_service.delete_invoice_payment(db, payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}
