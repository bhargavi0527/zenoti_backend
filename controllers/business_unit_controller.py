from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database.db import get_db
from schemas.business_unit_schema import BusinessUnitCreate, BusinessUnitUpdate, BusinessUnitResponse
from services import business_unit_service

router = APIRouter(prefix="/business-units", tags=["Business Units"])


@router.get("/", response_model=List[BusinessUnitResponse])
def list_business_units(db: Session = Depends(get_db)):
    return business_unit_service.get_all_business_units(db)


@router.get("/{bu_id}", response_model=BusinessUnitResponse)
def get_business_unit(bu_id: uuid.UUID, db: Session = Depends(get_db)):
    bu = business_unit_service.get_business_unit(db, bu_id)
    if not bu:
        raise HTTPException(status_code=404, detail="Business Unit not found")
    return bu


@router.post("/", response_model=BusinessUnitResponse)
def create_business_unit(bu: BusinessUnitCreate, db: Session = Depends(get_db)):
    return business_unit_service.create_business_unit(db, bu)


@router.put("/{bu_id}", response_model=BusinessUnitResponse)
def update_business_unit(bu_id: uuid.UUID, bu: BusinessUnitUpdate, db: Session = Depends(get_db)):
    updated = business_unit_service.update_business_unit(db, bu_id, bu)
    if not updated:
        raise HTTPException(status_code=404, detail="Business Unit not found")
    return updated


@router.delete("/{bu_id}", response_model=BusinessUnitResponse)
def delete_business_unit(bu_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted = business_unit_service.delete_business_unit(db, bu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business Unit not found")
    return deleted
