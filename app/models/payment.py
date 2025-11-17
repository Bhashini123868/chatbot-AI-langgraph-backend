from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Enum, DateTime, String, func
from sqlalchemy.orm import relationship
from ..models.base import Base
from ..models.enums import PaymentMethod

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(12,2), nullable=False)
    method = Column(Enum(PaymentMethod), default=PaymentMethod.cash)
    paid_at = Column(DateTime(timezone=True), server_default=func.now())
    transaction_ref = Column(String(255), nullable=True)

    order = relationship("Order", back_populates="payments")
