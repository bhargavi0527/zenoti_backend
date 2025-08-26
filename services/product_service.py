from sqlalchemy.orm import Session

from models import Product
from schemas.product_schema import ProductCreate, ProductUpdate
import uuid


def get_all_products(db: Session):
    return db.query(Product).all()


def create_product(db: Session, product: ProductCreate):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product(db: Session, product_id: uuid.UUID, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None

    for field, value in product.dict(exclude_unset=True).items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product
def delete_product(db: Session, product_id: uuid.UUID):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return True