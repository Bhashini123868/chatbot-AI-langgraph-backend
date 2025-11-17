from sqlalchemy import Column, Integer, String, Text, DateTime, func
from ..models.base import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50))
    email = Column(String(255))
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
