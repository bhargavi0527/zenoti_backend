# services/service_service.py
from sqlalchemy.orm import Session
from models import Service
from schemas.service_schema import ServiceCreate

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
