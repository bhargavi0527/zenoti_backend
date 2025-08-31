import uuid
from sqlalchemy.orm import Session
from models.category import Category
from schemas.category_schema import CategoryCreate, CategoryUpdate


def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category(db: Session, category_id: uuid.UUID):
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, category: CategoryCreate):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def update_category(db: Session, category_id: uuid.UUID, category: CategoryUpdate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None

    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: uuid.UUID):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None

    db.delete(db_category)
    db.commit()
    return db_category
