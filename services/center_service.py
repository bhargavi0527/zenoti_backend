# services/center_service.py
from sqlalchemy.orm import Session

from models import Center
from schemas.center_schema import CenterCreate

def create_center(db: Session, data: CenterCreate) -> Center:
    center = Center(**data.dict())
    db.add(center)
    db.commit()
    db.refresh(center)
    return center

def get_centers(db: Session):
    return db.query(Center).all()

def get_center(db: Session, center_id: str):
    return db.query(Center).filter(Center.id == center_id).first()
