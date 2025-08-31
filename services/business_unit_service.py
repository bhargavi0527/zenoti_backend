import uuid
from sqlalchemy.orm import Session
from models.business_unit import BusinessUnit
from schemas.business_unit_schema import BusinessUnitCreate, BusinessUnitUpdate


def get_all_business_units(db: Session):
    return db.query(BusinessUnit).all()


def get_business_unit(db: Session, bu_id: uuid.UUID):
    return db.query(BusinessUnit).filter(BusinessUnit.id == bu_id).first()


def create_business_unit(db: Session, bu: BusinessUnitCreate):
    new_bu = BusinessUnit(**bu.dict())
    db.add(new_bu)
    db.commit()
    db.refresh(new_bu)
    return new_bu


def update_business_unit(db: Session, bu_id: uuid.UUID, bu: BusinessUnitUpdate):
    db_bu = db.query(BusinessUnit).filter(BusinessUnit.id == bu_id).first()
    if not db_bu:
        return None

    for key, value in bu.dict(exclude_unset=True).items():
        setattr(db_bu, key, value)

    db.commit()
    db.refresh(db_bu)
    return db_bu


def delete_business_unit(db: Session, bu_id: uuid.UUID):
    db_bu = db.query(BusinessUnit).filter(BusinessUnit.id == bu_id).first()
    if not db_bu:
        return None

    db.delete(db_bu)
    db.commit()
    return db_bu
