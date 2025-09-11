import uuid
from datetime import datetime
from io import BytesIO

from reportlab.lib.units import mm
from sqlalchemy.orm import Session
from models import Invoice, Collection, Sale, InvoiceItem
from schemas.invoice_schema import InvoiceUpdate

# ReportLab (high level API, no canvas, no A4)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4


def generate_invoice_no(db: Session) -> str:
    """Generate unique invoice number, e.g. INV-2025-0001"""
    year = datetime.utcnow().year
    count = db.query(Invoice).count() + 1
    return f"INV-{year}-{count:04d}"


def create_invoice_from_sale(db: Session, sale_id: uuid.UUID) -> Invoice:
    """Create an invoice only if sale has payments."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise ValueError("Sale not found")

    if not sale.payments or len(sale.payments) == 0:
        raise ValueError("Cannot generate invoice without payment")

    invoice = Invoice(
        id=uuid.uuid4(),
        invoice_no=generate_invoice_no(db),
        invoice_date=datetime.utcnow().date(),
        invoice_date_full=datetime.utcnow(),
        gross_invoice_value=sale.gross_value,
        invoice_discount=sale.discount_value,
        net_invoice_value=sale.net_value,
        total_collection=sum(p.amount for p in sale.payments),
        sale_id=sale.id,
        guest_id=sale.appointment.guest_id if sale.appointment else None,
        employee_id=None,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def add_invoice_items(db: Session, invoice_id: uuid.UUID, items: list[dict]) -> list[InvoiceItem]:
    """Add items to an invoice."""
    invoice_items = []
    for idx, item in enumerate(items, start=1):
        inv_item = InvoiceItem(
            id=uuid.uuid4(),
            invoice_id=invoice_id,
            item_type=item.get("item_type"),
            item_code=item.get("item_code"),
            item_name=item.get("item_name"),
            item_tags=item.get("item_tags"),
            business_unit=item.get("business_unit"),
            category=item.get("category"),
            sub_category=item.get("sub_category"),
            item_quantity=item.get("item_quantity", 1),
            unit_price=item.get("unit_price", 0),
            item_discount=item.get("item_discount", 0),
            net_price=item.get("net_price", 0),
            row_num=idx,
            item_row_num=idx,
        )
        db.add(inv_item)
        invoice_items.append(inv_item)

    db.commit()
    return invoice_items


def get_invoices(db: Session):
    return db.query(Invoice).all()


def get_invoice(db: Session, invoice_id: uuid.UUID):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


def update_invoice(db: Session, invoice_id: uuid.UUID, invoice_update: InvoiceUpdate):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return None
    for key, value in invoice_update.dict(exclude_unset=True).items():
        setattr(invoice, key, value)
    db.commit()
    db.refresh(invoice)
    return invoice


def delete_invoice(db: Session, invoice_id: uuid.UUID):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if invoice:
        db.delete(invoice)
        db.commit()
    return invoice


def get_invoice_collections(db: Session, invoice_id: uuid.UUID):
    return db.query(Collection).filter(Collection.invoice_id == invoice_id).all()


def generate_invoice_pdf(db: Session, invoice: Invoice) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20 * mm, leftMargin=20 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm)

    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    bold = ParagraphStyle('Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10)
    italic = ParagraphStyle('Italic', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9)

    # ---------- Header ----------
    elements.append(Paragraph(f"Invoice No: <b>{invoice.invoice_no}</b>", bold))
    if invoice.invoice_date_full:
        elements.append(Paragraph(f"Date: {invoice.invoice_date_full.strftime('%d-%m-%Y %H:%M')}", styles["Normal"]))
    elements.append(Paragraph(f"Payment Status: <b>{getattr(invoice, 'payment_status', 'Pending')}</b>", bold))
    elements.append(Spacer(1, 12))

    # ---------- Guest Info ----------
    guest_name = f"{getattr(invoice.guest, 'first_name', '')} {getattr(invoice.guest, 'last_name', '')}".strip() if invoice.guest else ""
    if guest_name:
        elements.append(Paragraph(f"Guest: {guest_name}", styles["Normal"]))
    if getattr(invoice.guest, 'email', None):
        elements.append(Paragraph(f"Email: {invoice.guest.email}", styles["Normal"]))
    if getattr(invoice.guest, 'phone', None):
        elements.append(Paragraph(f"Phone: {invoice.guest.phone}", styles["Normal"]))
    if guest_name or getattr(invoice.guest, 'email', None) or getattr(invoice.guest, 'phone', None):
        elements.append(Spacer(1, 12))

    # ---------- Items Table ----------
    items = db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice.id).all()
    table_data = [["S.No", "Item", "Sub-description", "Doctor", "Qty", "Unit Price", "Discount", "Final Price"]]
    for idx, item in enumerate(items, start=1):
        doctor_name = getattr(item, "doctor_name", "-")  # Add doctor_name to InvoiceItem if exists
        sub_desc = getattr(item, "sub_description", "")
        table_data.append([
            idx,
            item.item_name or "",
            sub_desc,
            doctor_name,
            str(item.item_quantity),
            f"₹{item.unit_price:,.2f}",
            f"₹{item.item_discount:,.2f}",
            f"₹{item.net_price:,.2f}"
        ])

    table = Table(table_data, colWidths=[25 * mm, 60 * mm, 70 * mm, 40 * mm, 20 * mm, 30 * mm, 30 * mm, 30 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor('#d3d3d3')),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (4, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 15))

    # ---------- Totals ----------
    elements.append(Paragraph(f"Gross Value: ₹{invoice.gross_invoice_value:,.2f}", bold))
    elements.append(Paragraph(f"Discount: ₹{invoice.invoice_discount:,.2f}", bold))
    elements.append(Paragraph(f"Net Value: ₹{invoice.net_invoice_value:,.2f}", bold))
    elements.append(Paragraph(f"Total Collected: ₹{invoice.total_collection:,.2f}", bold))
    elements.append(Spacer(1, 20))

    # ---------- Footer ----------
    elements.append(Paragraph("Thank you for your business!", italic))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes