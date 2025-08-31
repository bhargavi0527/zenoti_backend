from sqlalchemy.orm import Session
from models import Service
from schemas.service_schema import ServiceCreate, ServiceUpdate
import uuid


def create_service(db: Session, data: ServiceCreate) -> Service:
    service = Service(**data.dict())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_services(db: Session):
    return db.query(Service).all()


def get_service(db: Session, service_id: str):
    return db.query(Service).filter(Service.id == service_id).first()


def update_service(db: Session, service_id: str, data: ServiceUpdate):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: str) -> bool:
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return False
    db.delete(service)
    db.commit()
    return True
