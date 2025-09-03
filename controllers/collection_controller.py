from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.collection_schema import (
    CollectionCreate, CollectionUpdate, CollectionResponse
)
from services import collection_service
from typing import List


router = APIRouter(prefix="/collections", tags=["Collections"])


@router.post("/", response_model=CollectionResponse)
def create_collection(collection: CollectionCreate, db: Session = Depends(get_db)):
    return collection_service.create_collection(db, collection)


@router.get("/", response_model=List[CollectionResponse])
def list_collections(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return collection_service.get_collections(db, skip, limit)


@router.get("/{col_id}", response_model=CollectionResponse)
def get_collection(col_id: str, db: Session = Depends(get_db)):
    collection = collection_service.get_collection(db, col_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.put("/{col_id}", response_model=CollectionResponse)
def update_collection(col_id: str, collection: CollectionUpdate, db: Session = Depends(get_db)):
    updated = collection_service.update_collection(db, col_id, collection)
    if not updated:
        raise HTTPException(status_code=404, detail="Collection not found")
    return updated


@router.delete("/{col_id}")
def delete_collection(col_id: str, db: Session = Depends(get_db)):
    deleted = collection_service.delete_collection(db, col_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Collection not found")
    return {"detail": "Collection deleted successfully"}
