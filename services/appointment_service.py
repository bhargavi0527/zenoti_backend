# services/appointment_service.py
from typing import List


from datetime import datetime, date
from typing import Optional
from sqlalchemy.orm import Session
from models import Appointment, Sale
from schemas.appointment_schema import AppointmentCreate
import uuid

def create_appointment(db: Session, data: AppointmentCreate) -> Appointment:
    appointment = Appointment(**data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # 🔹 Automatically create a Sale linked to this appointment
    sale = Sale(appointment_id=appointment.id, amount=0.0)
    db.add(sale)
    db.commit()
    db.refresh(sale)

    return appointment

def get_appointments(
    db: Session,
    status: Optional[str] = None,
    provider_id: Optional[uuid.UUID] = None,
    center_id: Optional[uuid.UUID] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
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

def get_appointment(db: Session, appointment_id: uuid.UUID):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def get_guest_appointments(db: Session, guest_id: uuid.UUID):
    return db.query(Appointment).filter(Appointment.guest_id == guest_id).all()

def get_center_appointments(db: Session, center_id: uuid.UUID):
    return db.query(Appointment).filter(Appointment.center_id == center_id).all()
def get_appointments_by_date(db: Session, appointment_date: date) -> List[Appointment]:
    """Fetch appointments for a specific date"""
    return (
        db.query(Appointment)
        .filter(Appointment.appointment_date == appointment_date)
        .all()
    )