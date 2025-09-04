from sqlalchemy.orm import Session
from models import Collection, Invoice
from schemas.collection_schema import CollectionCreate, CollectionUpdate
from datetime import datetime
import uuid

# 🔹 Helper to generate sequential collection numbers
def generate_collection_no(db: Session) -> str:
    year = datetime.now().year
    prefix = f"COLL-{year}-"

    # Get last collection for this year
    last_collection = (
        db.query(Collection)
        .filter(Collection.collection_no.like(f"{prefix}%"))
        .order_by(Collection.created_at.desc())
        .first()
    )

    if last_collection:
        last_no = int(last_collection.collection_no.split("-")[-1])
        new_no = last_no + 1
    else:
        new_no = 1

    return f"{prefix}{new_no:04d}"


def create_collection(db: Session, col_data: CollectionCreate) -> Collection:
    # 🔹 Always generate collection_no instead of taking from request
    collection_no = generate_collection_no(db)

    collection = Collection(
        id=uuid.uuid4(),
        collection_no=collection_no,
        **col_data.dict(exclude={"collection_no"})  # ignore client-sent number
    )
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
