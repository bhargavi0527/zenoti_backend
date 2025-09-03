import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models import Appointment, Guest
from schemas.appointment_schema import AppointmentRead
from schemas.center_schema import CenterCreate, CenterRead
from schemas.guest_schema import GuestResponse
from services.center_service import create_center, get_centers, get_center

router = APIRouter(prefix="/centers", tags=["Centers"])

@router.post("/", response_model=CenterRead)
def create_center_route(data: CenterCreate, db: Session = Depends(get_db)):
    return create_center(db, data)

@router.get("/", response_model=list[CenterRead])
def list_centers(db: Session = Depends(get_db)):
    return get_centers(db)

@router.get("/{center_id}", response_model=CenterRead)
def read_center(center_id: str, db: Session = Depends(get_db)):
    center = get_center(db, center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    return center
@router.get("/{center_id}/guests", response_model=list[GuestResponse])
def get_center_guests(center_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(Guest).filter(Guest.center_id == center_id).all()

@router.get("/{center_id}/appointments", response_model=list[AppointmentRead])
def get_center_appointments(center_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.center_id == center_id).all()