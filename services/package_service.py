import uuid
from sqlalchemy.orm import Session
from models.package import Package
from schemas.package_schema import PackageCreate, PackageUpdate


# Get all packages
def get_all_packages(db: Session):
    return db.query(Package).all()


# Get package by ID
def get_package(db: Session, package_id: uuid.UUID):
    return db.query(Package).filter(Package.id == package_id).first()


# Create new package
def create_package(db: Session, package: PackageCreate):
    new_package = Package(**package.dict())
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    return new_package


# Update package
def update_package(db: Session, package_id: uuid.UUID, package: PackageUpdate):
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        return None

    for key, value in package.dict(exclude_unset=True).items():
        setattr(db_package, key, value)

    db.commit()
    db.refresh(db_package)
    return db_package


# Delete package
def delete_package(db: Session, package_id: uuid.UUID):
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        return None

    db.delete(db_package)
    db.commit()
    return db_package
