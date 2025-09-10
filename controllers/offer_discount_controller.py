# controllers/offer_discount_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.offer_discount_schema import OfferDiscountCreate, OfferDiscountUpdate, OfferDiscountResponse
from services import offer_discount_service
from uuid import UUID

router = APIRouter(prefix="/offers-discounts", tags=["Offers & Discounts"])

@router.post("/", response_model=OfferDiscountResponse)
def create_offer_endpoint(offer: OfferDiscountCreate, db: Session = Depends(get_db)):
    return offer_discount_service.create_offer(db, offer)

@router.get("/", response_model=list[OfferDiscountResponse])
def list_offers(db: Session = Depends(get_db)):
    return offer_discount_service.get_offers(db)

@router.get("/{offer_id}", response_model=OfferDiscountResponse)
def get_offer_endpoint(offer_id: UUID, db: Session = Depends(get_db)):
    offer = offer_discount_service.get_offer(db, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.put("/{offer_id}", response_model=OfferDiscountResponse)
def update_offer_endpoint(offer_id: UUID, offer_data: OfferDiscountUpdate, db: Session = Depends(get_db)):
    offer = offer_discount_service.update_offer(db, offer_id, offer_data)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer

@router.delete("/{offer_id}")
def delete_offer_endpoint(offer_id: UUID, db: Session = Depends(get_db)):
    success = offer_discount_service.delete_offer(db, offer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Offer not found")
    return {"message": "Offer deleted successfully"}
