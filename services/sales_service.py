import uuid
from sqlalchemy.orm import Session
from models import Sale, Invoice, Appointment
from schemas.sales_schema import SaleCreate, SaleUpdate


def create_sale(db: Session, sale_data: SaleCreate) -> Sale:
    # 1. Fetch appointment
    appointment = db.query(Appointment).filter(Appointment.id == sale_data.appointment_id).first()
    if not appointment:
        raise ValueError("Appointment not found")

    # 2. Automatically generate sale_no
    sale_no = f"SALE-{uuid.uuid4().hex[:8]}"

    # 3. Create sale based on appointment values
    sale = Sale(
        sale_no=sale_no,
        gross_value=appointment.gross_value,
        discount_value=appointment.discount_value,
        net_value=appointment.net_value,
        remarks=sale_data.remarks,
        appointment_id=appointment.id
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)

    # # 4. Create invoice automatically
    # invoice = Invoice(
    #     id=uuid.uuid4(),
    #     invoice_no=f"INV-{sale.sale_no}",
    #     sale_id=sale.id,
    #     appointment_id=appointment.id,
    #     amount_due=sale.net_value,
    #     status="UNPAID"
    # )
    # db.add(invoice)
    # db.commit()
    # db.refresh(invoice)
    #
    # # Attach invoice for response
    # sale.invoice = invoice
    # return sale

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
