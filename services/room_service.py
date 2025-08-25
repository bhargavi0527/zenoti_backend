from sqlalchemy.orm import Session
from models import Room
from schemas.room_schema import RoomCreate, RoomUpdate
from uuid import UUID


def get_all_rooms(db: Session):
    return db.query(Room).all()


def get_room_by_id(db: Session, room_id: UUID):
    return db.query(Room).filter(Room.id == room_id).first()


def create_room(db: Session, room_data: RoomCreate):
    new_room = Room(**room_data.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


def update_room(db: Session, room_id: UUID, room_data: RoomUpdate):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None
    for key, value in room_data.dict(exclude_unset=True).items():
        setattr(room, key, value)
    db.commit()
    db.refresh(room)
    return room


def delete_room(db: Session, room_id: UUID):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return None
    db.delete(room)
    db.commit()
    return room
