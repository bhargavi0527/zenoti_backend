from sqlalchemy.orm import Session
from models import Sale, Invoice
from schemas.sales_schema import SaleCreate, SaleUpdate
import uuid

def create_sale(db: Session, sale_data: SaleCreate) -> Sale:
    # ✅ Create Sale
    sale = Sale(
        sale_no=sale_data.sale_no,
        gross_value=sale_data.gross_value,
        discount_value=sale_data.discount_value,
        net_value=sale_data.net_value,
        remarks=sale_data.remarks,
        appointment_id=sale_data.appointment_id,

    )
    db.add(sale)
    db.commit()
    db.refresh(sale)

    # ✅ Automatically create Invoice for this Sale
    invoice = Invoice(
        id=uuid.uuid4(),
        invoice_no=f"INV-{sale.sale_no}",  # Example: INV-SALE-1001
        sale_id=sale.id,
        appointment_id=sale.appointment_id,
        amount_due=sale.net_value,
        status="UNPAID"   # default status
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    # attach invoice to sale object (for response)
    sale.invoice = invoice

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
