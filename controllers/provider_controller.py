# routers/provider_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.provider_schema import ProviderCreate, ProviderRead
from services.provider_service import create_provider, get_providers, get_provider

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.post("/", response_model=ProviderRead)
def create_provider_route(data: ProviderCreate, db: Session = Depends(get_db)):
    return create_provider(db, data)

@router.get("/", response_model=list[ProviderRead])
def list_providers(db: Session = Depends(get_db)):
    return get_providers(db)

@router.get("/{provider_id}", response_model=ProviderRead)
def read_provider(provider_id: str, db: Session = Depends(get_db)):
    provider = get_provider(db, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider
