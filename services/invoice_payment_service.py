from sqlalchemy.orm import Session
from models.invoice_payment import InvoicePayment
from schemas.invoice_payment_schema import InvoicePaymentCreate, InvoicePaymentUpdate
import uuid


def create_invoice_payment(db: Session, payment: InvoicePaymentCreate):
    """Create a new payment entry for an invoice"""
    new_payment = InvoicePayment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


def get_payments_by_invoice(db: Session, invoice_id: uuid.UUID):
    """Fetch all payments belonging to a specific invoice"""
    return db.query(InvoicePayment).filter(InvoicePayment.invoice_id == invoice_id).all()


def get_invoice_payment(db: Session, payment_id: uuid.UUID):
    """Fetch a single payment by its ID"""
    return db.query(InvoicePayment).filter(InvoicePayment.id == payment_id).first()


def update_invoice_payment(db: Session, payment_id: uuid.UUID, payment_update: InvoicePaymentUpdate):
    """Update an existing payment"""
    payment = db.query(InvoicePayment).filter(InvoicePayment.id == payment_id).first()
    if not payment:
        return None
    for key, value in payment_update.dict(exclude_unset=True).items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment


def delete_invoice_payment(db: Session, payment_id: uuid.UUID):
    """Delete a payment by ID"""
    payment = db.query(InvoicePayment).filter(InvoicePayment.id == payment_id).first()
    if payment:
        db.delete(payment)
        db.commit()
    return payment
