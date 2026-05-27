import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.database import Base


class UserRole(str, enum.Enum):
    EMPLOYEE = "employee"
    COMPLIANCE_OFFICER = "compliance_officer"
    EXECUTIVE = "executive"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
