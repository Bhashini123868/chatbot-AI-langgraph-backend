from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from ..models.base import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(DECIMAL(10,2), nullable=False)
    subtotal = Column(DECIMAL(12,2), nullable=False)
    notes = Column(Text)

    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")
