from sqlalchemy.orm import Session
from models.guest import Guest
from schemas.guest_schema import GuestCreate
from typing import Optional

# ✅ CREATE
def create_guest(db: Session, guest_data: GuestCreate) -> Guest:
    db_guest = Guest(**guest_data.dict())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

# ✅ READ (by email)
def get_guest_by_email(db: Session, email: str) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.email == email).first()

# ✅ READ (list all)
def get_guests(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Guest).offset(skip).limit(limit).all()

# ✅ READ (by guest_code)
def get_guest_by_code(db: Session, guest_code: str) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.guest_code == guest_code).first()

# ✅ READ (by id)
def get_guest_by_id(db: Session, guest_id: str) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.id == guest_id).first()

# ✅ UPDATE (by id)
def update_guest(db: Session, guest_id: str, update_data: dict) -> Optional[Guest]:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        return None
    for key, value in update_data.items():
        if hasattr(guest, key) and value is not None:
            setattr(guest, key, value)
    db.commit()
    db.refresh(guest)
    return guest

# ✅ DELETE (by id)
def delete_guest(db: Session, guest_id: str) -> bool:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        return False
    db.delete(guest)
    db.commit()
    return True
