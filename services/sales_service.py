import uuid
from datetime import datetime
from decimal import Decimal   # ✅ add this
from sqlalchemy.orm import Session
from models import Sale, Invoice, Appointment, OfferDiscount, Product, Package, Service
from schemas.sales_schema import SaleCreate, SaleUpdate


def create_sale(db: Session, sale_data: SaleCreate) -> Sale:
    # 1️⃣ Fetch appointment
    appointment = db.query(Appointment).filter(Appointment.id == sale_data.appointment_id).first()
    if not appointment:
        raise ValueError("Appointment not found")

    # 2️⃣ Fetch item and determine gross value
    item = None
    gross_value = Decimal(0)

    if sale_data.item_type == "product":
        item = db.query(Product).filter(Product.id == sale_data.item_id).first()
        if not item:
            raise ValueError("Product not found")
        gross_value = Decimal(item.mrp)

    elif sale_data.item_type == "service":
        item = db.query(Service).filter(Service.id == sale_data.item_id).first()
        if not item:
            raise ValueError("Service not found")
        gross_value = Decimal(item.price)  # ✅ wrap as Decimal

    elif sale_data.item_type == "package":
        item = db.query(Package).filter(Package.id == sale_data.item_id).first()
        if not item:
            raise ValueError("Package not found")
        gross_value = Decimal(item.series_package_cost_to_center)  # ✅ wrap as Decimal

    else:
        raise ValueError("Invalid item_type")

    # 3️⃣ Apply discount if exists
    discount_value = Decimal(0)
    if sale_data.discount_id:
        discount = db.query(OfferDiscount).filter(OfferDiscount.id == sale_data.discount_id).first()
        if discount:
            if discount.discount_type == "fixed":
                discount_value = Decimal(discount.discount_value)
            elif discount.discount_type == "percentage":
                discount_value = gross_value * (Decimal(discount.discount_value) / Decimal(100))

    # 4️⃣ Calculate net
    net_value = gross_value - discount_value

    # 5️⃣ Create sale
    sale = Sale(
        sale_no=f"SALE-{uuid.uuid4().hex[:8]}",
        gross_value=gross_value,
        discount_value=discount_value,
        net_value=net_value,
        appointment_id=appointment.id,
        discount_id=sale_data.discount_id,
        remarks=sale_data.remarks
    )

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return sale


def get_sale(db: Session, sale_id: uuid.UUID) -> Sale | None:
    return db.query(Sale).filter(Sale.id == sale_id).first()


def get_sales(db: Session):
    return db.query(Sale).all()


def update_sale(db: Session, sale_id: uuid.UUID, sale_data: SaleUpdate) -> Sale | None:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        return None
    for key, value in sale_data.dict(exclude_unset=True).items():
        setattr(sale, key, value)
    db.commit()
    db.refresh(sale)
    return sale


def delete_sale(db: Session, sale_id: uuid.UUID) -> bool:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        return False
    db.delete(sale)
    db.commit()
    return True


# 🔹 Relationship helpers
def get_sale_invoice(db: Session, sale_id: uuid.UUID) -> Invoice | None:
    return db.query(Invoice).filter(Invoice.sale_id == sale_id).first()
