from sqlalchemy.orm import Session
from models import Guest, Appointment, Invoice
from schemas.guest_schema import GuestCreate
from typing import Optional
import uuid

def create_guest(db: Session, guest_data: GuestCreate) -> Guest:
    db_guest = Guest(**guest_data.dict())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest
def get_guests(db: Session):
    return db.query(Guest).all()

def get_guest_by_id(db: Session, guest_id: uuid.UUID) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.id == guest_id).first()

def get_guest_by_email(db: Session, email: str) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.email == email).first()

def get_guest_by_code(db: Session, guest_code: str) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.guest_code == guest_code).first()


def update_guest(db: Session, guest_id: uuid.UUID, update_data: dict) -> Optional[Guest]:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        return None
    for key, value in update_data.items():
        if hasattr(guest, key) and value is not None:
            setattr(guest, key, value)
    db.commit()
    db.refresh(guest)
    return guest

def delete_guest(db: Session, guest_id: uuid.UUID) -> bool:
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        return False
    db.delete(guest)
    db.commit()
    return True

# 🔹 Relationship helpers
def get_guest_appointments(db: Session, guest_id: uuid.UUID):
    return db.query(Appointment).filter(Appointment.guest_id == guest_id).all()

def get_guest_invoices(db: Session, guest_id: uuid.UUID):
    return db.query(Invoice).filter(Invoice.guest_id == guest_id).all()
