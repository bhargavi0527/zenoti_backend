# controllers/guest_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.guest_schema import GuestCreate, GuestResponse
from services.guest_service import create_guest, get_guests, get_guest_by_email

router = APIRouter(prefix="/guests", tags=["Guests"])


@router.post("/", response_model=GuestResponse)
def register_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    existing_guest = get_guest_by_email(db, email=guest.email)
    if existing_guest:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_guest(db, guest)


@router.get("/", response_model=list[GuestResponse])
def list_guests(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_guests(db, skip=skip, limit=limit)
