from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.exceptions import AuthenticationError
from app.schemas.user import UserCreate
from datetime import timedelta
from app.core.config import settings

class AuthService:
    """
    Service para autenticação

    Responsabilidades:
    - Autenticar usuário
    - Gerar tokens JWT
    - Registrar novos usuários
    """

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def authenticate_user(self, username: str, password: str) -> User:
        """Autentica usuário e retorna o User object"""
        user = self.user_repo.get_by_username(username)

        if not user:
            raise AuthenticationError("Usuário ou senha incorretos")

        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Usuário ou senha incorretos")

        if not user.is_active:
            raise AuthenticationError("Usuário inativo")

        return user

    def create_token(self, user: User) -> str:
        """Cria token JWT para usuário"""
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        token_data = {
            "sub": user.username,
            "user_id": user.id,
            "email": user.email
        }

        return create_access_token(token_data, access_token_expires)

    def register_user(self, user_data: UserCreate) -> User:
        """Registra novo usuário"""
        # Verificar se já existe
        if self.user_repo.get_by_email(user_data.email):
            raise AuthenticationError("Email já cadastrado")

        if self.user_repo.get_by_username(user_data.username):
            raise AuthenticationError("Username já cadastrado")

        return self.user_repo.create(user_data)
