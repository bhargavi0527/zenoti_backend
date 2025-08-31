from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.db import get_db
from models.appointment import Appointment
from schemas.appointment_schema import AppointmentCreate, AppointmentRead, AppointmentResponse, AppointmentUpdate
from uuid import uuid4
from datetime import datetime, date

from services.appointment_service import get_appointments, get_appointments_by_date

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("/", response_model=List[AppointmentRead])
def list_appointments(db: Session = Depends(get_db)):
    """Fetch all appointments"""
    return get_appointments(db)

@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    # Auto-derive appointment_date if not provided
    appointment_date = appointment.appointment_date or appointment.scheduled_time.date()

    db_appointment = Appointment(
        id=uuid4(),
        center_id=appointment.center_id,
        provider_id=appointment.provider_id,
        service_id=appointment.service_id,
        status=appointment.status,
        notes=appointment.notes,
        scheduled_time=appointment.scheduled_time,
        appointment_date=appointment_date,   # ✅ new field
        guest_id=appointment.guest_id,       # ✅ only guest_id
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return AppointmentResponse(
        **db_appointment.__dict__,
        message="Appointment created successfully"
    )


@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(appointment_id: str, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment_endpoint(
    appointment_id: str,
    update_data: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment).filter(Appointment.id == appointment_id).first()
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if update_data.scheduled_time:
        appointment.scheduled_time = update_data.scheduled_time
        # auto-update appointment_date if not explicitly provided
        if not update_data.appointment_date:
            appointment.appointment_date = update_data.scheduled_time.date()

    if update_data.appointment_date:
        appointment.appointment_date = update_data.appointment_date

    appointment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(appointment)

    return AppointmentResponse(
        **appointment.__dict__,
        message="Appointment updated successfully"
    )
@router.get("/slots/", response_model=List[AppointmentRead])
def get_slots_by_date(
    appointment_date: date = Query(..., description="Date in YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """Fetch appointment slots for a given date"""
    appointments = get_appointments_by_date(db, appointment_date)
    return appointments