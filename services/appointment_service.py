# services/appointment_service.py
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from models import Appointment
from schemas.appointment_schema import AppointmentCreate

def create_appointment(db: Session, data: AppointmentCreate) -> Appointment:
    appointment = Appointment(**data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_appointments(
    db: Session,
    status: Optional[str] = None,
    provider_id: Optional[str] = None,
    center_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = db.query(Appointment)

    if status:
        query = query.filter(Appointment.status == status)
    if provider_id:
        query = query.filter(Appointment.provider_id == provider_id)
    if center_id:
        query = query.filter(Appointment.center_id == center_id)
    if start_date:
        query = query.filter(Appointment.scheduled_time >= start_date)
    if end_date:
        query = query.filter(Appointment.scheduled_time <= end_date)

    return query.all()

def get_appointment(db: Session, appointment_id: str):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()
def update_appointment(
    db: Session, appointment_id: str, data: dict
) -> Optional[Appointment]:
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        return None

    if "scheduled_time" in data and data["scheduled_time"]:
        appointment.scheduled_time = data["scheduled_time"]
        # If appointment_date not provided, auto-derive from scheduled_time
        if "appointment_date" not in data or not data["appointment_date"]:
            appointment.appointment_date = data["scheduled_time"].date()

    if "appointment_date" in data and data["appointment_date"]:
        appointment.appointment_date = data["appointment_date"]

    appointment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(appointment)
    return appointment
