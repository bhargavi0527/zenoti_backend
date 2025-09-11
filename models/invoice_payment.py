from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.db import Base
import uuid


class InvoicePayment(Base):
    __tablename__ = "invoice_payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    payment_method = Column(String, nullable=False)  # e.g. cash, card, upi, gift_card
    amount = Column(Float, default=0)
    transaction_no = Column(String, nullable=True)   # UTR, card txn id, cheque no, etc.
    reference_no = Column(String, nullable=True)
    remarks = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ⬇️ Belongs to Sale (NOT Invoice directly anymore)
    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id"), nullable=False)
    sale = relationship("Sale", back_populates="payments")