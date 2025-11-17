from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from ..models.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    unit = Column(String(50), nullable=False)
    quantity = Column(DECIMAL(12,3), nullable=False, default=0)
    threshold = Column(DECIMAL(12,3), default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
