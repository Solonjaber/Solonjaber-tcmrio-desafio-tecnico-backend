from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Schema base para usuário"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    """Schema para criação de usuário"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """Schema para usuário no banco"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    """Schema para resposta de usuário"""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
