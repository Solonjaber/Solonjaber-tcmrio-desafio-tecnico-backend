from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationError
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registra novo usuário

    - **email**: Email válido
    - **username**: Nome de usuário único
    - **password**: Senha (mínimo 8 caracteres)
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.register_user(user_data)
        return user
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login e geração de token JWT

    - **username**: Nome de usuário
    - **password**: Senha
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        token = auth_service.create_token(user)

        return {"access_token": token, "token_type": "bearer"}
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Retorna informações do usuário autenticado

    Requer autenticação via token JWT
    """
    return current_user
