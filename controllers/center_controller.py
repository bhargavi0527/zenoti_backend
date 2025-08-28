from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.center_schema import CenterCreate, CenterRead
from services.center_service import create_center, get_centers, get_center

router = APIRouter(prefix="/centers", tags=["Centers"])

@router.post("/", response_model=CenterRead)
def create_center_route(data: CenterCreate, db: Session = Depends(get_db)):
    return create_center(db, data)

@router.get("/", response_model=list[CenterRead])
def list_centers(db: Session = Depends(get_db)):
    return get_centers(db)

@router.get("/{center_id}", response_model=CenterRead)
def read_center(center_id: str, db: Session = Depends(get_db)):
    center = get_center(db, center_id)
    if not center:
        raise HTTPException(status_code=404, detail="Center not found")
    return center
