# services/guest_service.py
from sqlalchemy.orm import Session
from models.guest import Guest
from schemas.guest_schema import GuestCreate


def create_guest(db: Session, guest_data: GuestCreate) -> Guest:
    db_guest = Guest(**guest_data.dict())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest


def get_guest_by_email(db: Session, email: str) -> Guest | None:
    return db.query(Guest).filter(Guest.email == email).first()


def get_guests(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Guest).offset(skip).limit(limit).all()
