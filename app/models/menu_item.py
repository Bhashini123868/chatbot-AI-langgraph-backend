from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from ..models.base import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    price = Column(DECIMAL(10,2), nullable=False)
    is_available = Column(Boolean, default=True)
    prep_time_minutes = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", backref="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")
