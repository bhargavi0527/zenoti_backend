# services/offer_discount_service.py
from sqlalchemy.orm import Session
from models.offer_discount import OfferDiscount
from schemas.offer_discount_schema import OfferDiscountCreate, OfferDiscountUpdate
import uuid

def create_offer(db: Session, offer_data: OfferDiscountCreate) -> OfferDiscount:
    offer = OfferDiscount(
        id=uuid.uuid4(),
        item_type=offer_data.item_type,
        item_id=offer_data.item_id,
        discount_type=offer_data.discount_type,
        discount_value=offer_data.discount_value,
        description=offer_data.description
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer

def get_offer(db: Session, offer_id: uuid.UUID):
    return db.query(OfferDiscount).filter(OfferDiscount.id == offer_id).first()

def get_offers(db: Session):
    return db.query(OfferDiscount).all()

def update_offer(db: Session, offer_id: uuid.UUID, offer_data: OfferDiscountUpdate):
    offer = db.query(OfferDiscount).filter(OfferDiscount.id == offer_id).first()
    if not offer:
        return None
    for key, value in offer_data.dict(exclude_unset=True).items():
        setattr(offer, key, value)
    db.commit()
    db.refresh(offer)
    return offer

def delete_offer(db: Session, offer_id: uuid.UUID):
    offer = db.query(OfferDiscount).filter(OfferDiscount.id == offer_id).first()
    if not offer:
        return False
    db.delete(offer)
    db.commit()
    return True
