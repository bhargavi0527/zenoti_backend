from sqlalchemy.orm import Session
from models import RoomCategory
from schemas.room_category_schema import RoomCategoryCreate, RoomCategoryUpdate
from uuid import UUID


def get_all_categories(db: Session):
    return db.query(RoomCategory).all()


def get_category_by_id(db: Session, category_id: UUID):
    return db.query(RoomCategory).filter(RoomCategory.id == category_id).first()


def create_category(db: Session, category_data: RoomCategoryCreate):
    new_category = RoomCategory(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def update_category(db: Session, category_id: UUID, category_data: RoomCategoryUpdate):
    category = db.query(RoomCategory).filter(RoomCategory.id == category_id).first()
    if not category:
        return None
    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: UUID):
    category = db.query(RoomCategory).filter(RoomCategory.id == category_id).first()
    if not category:
        return None
    db.delete(category)
    db.commit()
    return category
