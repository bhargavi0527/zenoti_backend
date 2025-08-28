from sqlalchemy.orm import Session

from models import InvoiceItem
from schemas.invoice_item_schema import InvoiceItemCreate, InvoiceItemUpdate
import uuid


def create_invoice_item(db: Session, item: InvoiceItemCreate):
    new_item = InvoiceItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_items_by_invoice(db: Session, invoice_id: uuid.UUID):
    return db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).all()


def get_invoice_item(db: Session, item_id: uuid.UUID):
    return db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()


def update_invoice_item(db: Session, item_id: uuid.UUID, item_update: InvoiceItemUpdate):
    item = db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()
    if not item:
        return None
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


def delete_invoice_item(db: Session, item_id: uuid.UUID):
    item = db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item
