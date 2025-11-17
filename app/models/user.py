from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from ..models.base import Base
from ..models.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.staff)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
