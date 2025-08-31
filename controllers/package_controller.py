from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from database.db import get_db
from schemas.package_schema import PackageCreate, PackageUpdate, PackageResponse
from services import package_service

router = APIRouter(prefix="/packages", tags=["Packages"])


@router.get("/", response_model=List[PackageResponse])
def list_packages(db: Session = Depends(get_db)):
    return package_service.get_all_packages(db)


@router.get("/{package_id}", response_model=PackageResponse)
def get_package(package_id: uuid.UUID, db: Session = Depends(get_db)):
    package = package_service.get_package(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package


@router.post("/", response_model=PackageResponse)
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    return package_service.create_package(db, package)


@router.put("/{package_id}", response_model=PackageResponse)
def update_package(package_id: uuid.UUID, package: PackageUpdate, db: Session = Depends(get_db)):
    updated = package_service.update_package(db, package_id, package)
    if not updated:
        raise HTTPException(status_code=404, detail="Package not found")
    return updated


@router.delete("/{package_id}", response_model=PackageResponse)
def delete_package(package_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted = package_service.delete_package(db, package_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Package not found")
    return deleted
