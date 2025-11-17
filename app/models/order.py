from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from ..models.base import Base
from ..models.enums import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    table_no = Column(String(50), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_amount = Column(DECIMAL(12,2), default=0)
    placed_at = Column(DateTime(timezone=True), server_default=func.now())
    served_at = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    customer = relationship("Customer", backref="orders")
    created_by_user = relationship("User", backref="orders_created")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
