from datetime import datetime

from sqlalchemy.orm import Session
from models import Invoice, Collection, Sale, sale
from schemas.invoice_schema import InvoiceCreate, InvoiceUpdate
import uuid


def generate_invoice_no(db: Session) -> str:
    # Example: INV-2025-0001
    year = datetime.utcnow().year
    count = db.query(Invoice).count() + 1
    return f"INV-{year}-{count:04d}"


def create_invoice(db: Session, sale_id: uuid.UUID) -> Invoice:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise ValueError("Sale not found")

    invoice = Invoice(
        id=uuid.uuid4(),
        invoice_no=f"INV-{sale.sale_no}-{str(uuid.uuid4())[:8]}",
        sale_id=sale.id,
        net_invoice_value=sale.net_value,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    return invoice

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

# 🔹 Relationship helpers
def get_invoice_collections(db: Session, invoice_id: uuid.UUID):
    return db.query(Collection).filter(Collection.invoice_id == invoice_id).all()
