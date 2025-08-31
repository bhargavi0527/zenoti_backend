# routers/service_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.service_schema import ServiceCreate, ServiceRead, ServiceUpdate
from services.service_services import (
    create_service,
    get_service,
    get_services,
    update_service,
    delete_service,
)

router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceRead)
def create_service_route(data: ServiceCreate, db: Session = Depends(get_db)):
    return create_service(db, data)


@router.get("/", response_model=list[ServiceRead])
def list_services(db: Session = Depends(get_db)):
    return get_services(db)


@router.get("/{service_id}", response_model=ServiceRead)
def read_service(service_id: str, db: Session = Depends(get_db)):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.put("/{service_id}", response_model=ServiceRead)
def update_service_route(service_id: str, data: ServiceUpdate, db: Session = Depends(get_db)):
    service = update_service(db, service_id, data)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@router.delete("/{service_id}")
def delete_service_route(service_id: str, db: Session = Depends(get_db)):
    deleted = delete_service(db, service_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}
