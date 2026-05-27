from pydantic import BaseModel, EmailStr
from app.models.user import UserRole
from datetime import datetime


# --- Request Schemas ---

class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole = UserRole.EMPLOYEE


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRoleUpdate(BaseModel):
    role: UserRole


# --- Response Schemas ---

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse