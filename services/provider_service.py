# services/provider_service.py
from sqlalchemy.orm import Session

from models import Provider
from schemas.provider_schema import ProviderCreate

def create_provider(db: Session, data: ProviderCreate) -> Provider:
    provider = Provider(**data.dict())
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider

def get_providers(db: Session):
    return db.query(Provider).all()

def get_provider(db: Session, provider_id: str):
    return db.query(Provider).filter(Provider.id == provider_id).first()
