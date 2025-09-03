from sqlalchemy.orm import Session
from models import Collection, Invoice
from schemas.collection_schema import CollectionCreate, CollectionUpdate
import uuid

def create_collection(db: Session, col_data: CollectionCreate) -> Collection:
    collection = Collection(**col_data.dict())
    db.add(collection)

    # 🔹 Auto-update invoice status
    invoice = db.query(Invoice).filter(Invoice.id == collection.invoice_id).first()
    if invoice:
        total_paid = sum(c.amount for c in invoice.collections) + collection.amount
        if total_paid >= invoice.total_amount:
            invoice.status = "PAID"

    db.commit()
    db.refresh(collection)
    return collection

def get_collection(db: Session, col_id: uuid.UUID) -> Collection | None:
    return db.query(Collection).filter(Collection.id == col_id).first()

def get_collections(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Collection).offset(skip).limit(limit).all()

def update_collection(db: Session, col_id: uuid.UUID, col_data: CollectionUpdate) -> Collection | None:
    collection = db.query(Collection).filter(Collection.id == col_id).first()
    if not collection:
        return None
    for key, value in col_data.dict(exclude_unset=True).items():
        setattr(collection, key, value)
    db.commit()
    db.refresh(collection)
    return collection

def delete_collection(db: Session, col_id: uuid.UUID) -> bool:
    collection = db.query(Collection).filter(Collection.id == col_id).first()
    if not collection:
        return False
    db.delete(collection)
    db.commit()
    return True
