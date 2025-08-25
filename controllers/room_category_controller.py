from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from database.db import get_db
from schemas.room_category_schema import (
    RoomCategoryCreate,
    RoomCategoryUpdate,
    RoomCategoryOut,
)
from services import room_category_service

router = APIRouter(prefix="/room-categories", tags=["Room Categories"])


@router.get("/", response_model=list[RoomCategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return room_category_service.get_all_categories(db)


@router.get("/{category_id}", response_model=RoomCategoryOut)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    category = room_category_service.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=RoomCategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category: RoomCategoryCreate, db: Session = Depends(get_db)):
    return room_category_service.create_category(db, category)


@router.put("/{category_id}", response_model=RoomCategoryOut)
def update_category(category_id: UUID, category: RoomCategoryUpdate, db: Session = Depends(get_db)):
    updated = room_category_service.update_category(db, category_id, category)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    deleted = room_category_service.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return None
