from sqlalchemy.orm import Session
from models.invoice import Invoice
from schemas.invoice_schema import InvoiceCreate, InvoiceUpdate
import uuid


def create_invoice(db: Session, invoice: InvoiceCreate):
    new_invoice = Invoice(**invoice.dict())
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


def get_invoices(db: Session):
    return db.query(Invoice).all()


def get_invoice(db: Session, invoice_id: uuid.UUID):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


def update_invoice(db: Session, invoice_id: uuid.UUID, invoice_update: InvoiceUpdate):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return None
    for key, value in invoice_update.dict(exclude_unset=True).items():
        setattr(invoice, key, value)
    db.commit()
    db.refresh(invoice)
    return invoice


def delete_invoice(db: Session, invoice_id: uuid.UUID):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if invoice:
        db.delete(invoice)
        db.commit()
    return invoice
