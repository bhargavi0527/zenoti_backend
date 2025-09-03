from sqlalchemy.orm import Session
from models import Center, Guest, Appointment
from schemas.center_schema import CenterCreate
import uuid

def create_center(db: Session, data: CenterCreate) -> Center:
    center = Center(**data.dict())
    db.add(center)
    db.commit()
    db.refresh(center)
    return center

def get_centers(db: Session):
    return db.query(Center).all()

def get_center(db: Session, center_id: uuid.UUID):
    return db.query(Center).filter(Center.id == center_id).first()

# 🔹 Relationship helpers
def get_center_guests(db: Session, center_id: uuid.UUID):
    return db.query(Guest).filter(Guest.center_id == center_id).all()

def get_center_appointments(db: Session, center_id: uuid.UUID):
    return db.query(Appointment).filter(Appointment.center_id == center_id).all()
