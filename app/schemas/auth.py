from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    """Schema para resposta de token JWT"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema para dados extraídos do token"""
    username: str | None = None

class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    username: str
    password: str
