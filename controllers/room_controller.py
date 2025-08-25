from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from database.db import get_db
from schemas.room_schema import RoomCreate, RoomUpdate, RoomOut
from services import room_service

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=list[RoomOut])
def list_rooms(db: Session = Depends(get_db)):
    return room_service.get_all_rooms(db)


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: UUID, db: Session = Depends(get_db)):
    room = room_service.get_room_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


@router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return room_service.create_room(db, room)


@router.put("/{room_id}", response_model=RoomOut)
def update_room(room_id: UUID, room: RoomUpdate, db: Session = Depends(get_db)):
    updated = room_service.update_room(db, room_id, room)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return updated


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: UUID, db: Session = Depends(get_db)):
    deleted = room_service.delete_room(db, room_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return None
