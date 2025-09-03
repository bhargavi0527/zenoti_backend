import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models import Appointment, Invoice
from schemas.appointment_schema import AppointmentRead
from schemas.guest_schema import GuestCreate, GuestResponse, GuestUpdate
from schemas.invoice_schema import InvoiceOut
from services.guest_service import (
    create_guest, get_guests, get_guest_by_email,
    get_guest_by_code, get_guest_by_id,
    update_guest, delete_guest
)

router = APIRouter(prefix="/guests", tags=["Guests"])

# ✅ CREATE
@router.post("/", response_model=GuestResponse)
def register_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    existing_guest = get_guest_by_email(db, email=guest.email)
    if existing_guest:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_guest(db, guest)

@router.get("/", response_model=list[GuestResponse])
def list_guests(db: Session = Depends(get_db)):
    return get_guests(db)

# ✅ READ by id
@router.get("/{guest_id}", response_model=GuestResponse)
def fetch_guest_by_id(guest_id: str, db: Session = Depends(get_db)):
    guest = get_guest_by_id(db, guest_id)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

# ✅ READ by guest_code
@router.get("/code/{guest_code}", response_model=GuestResponse)
def fetch_guest_by_code(guest_code: str, db: Session = Depends(get_db)):
    guest = get_guest_by_code(db, guest_code)
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return guest

# ✅ UPDATE by id
@router.put("/{guest_id}", response_model=GuestResponse)
def update_guest_route(guest_id: str, guest_update: GuestUpdate, db: Session = Depends(get_db)):
    updated_guest = update_guest(db, guest_id, guest_update.dict(exclude_unset=True))
    if not updated_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
    return updated_guest

# ✅ DELETE by id
@router.delete("/{guest_id}")
def delete_guest_route(guest_id: str, db: Session = Depends(get_db)):
    success = delete_guest(db, guest_id)
    if not success:
        raise HTTPException(status_code=404, detail="Guest not found")
    return {"detail": "Guest deleted successfully"}
@router.get("/{guest_id}/appointments", response_model=list[AppointmentRead])
def get_guest_appointments(guest_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.guest_id == guest_id).all()

@router.get("/{guest_id}/invoices", response_model=list[InvoiceOut])
def get_guest_invoices(guest_id: uuid.UUID, db: Session = Depends(get_db)):
    return db.query(Invoice).filter(Invoice.guest_id == guest_id).all()