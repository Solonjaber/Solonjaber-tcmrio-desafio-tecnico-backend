"""
Script para criar usuário admin padrão
Nota: As migrations são gerenciadas pelo Alembic
"""
from app.core.security import get_password_hash
from app.db.database import SessionLocal
import logging

# Importar todos os modelos para resolver relacionamentos
from app.db.base import *  # noqa
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Cria usuário admin padrão se não existir"""
    try:
        # Criar usuário admin padrão
        logger.info("Verificando usuário admin...")
        db = SessionLocal()
        try:
            admin = db.query(User).filter(User.email == "admin@example.com").first()
            if not admin:
                logger.info("Criando usuário admin...")
                admin = User(
                    email="admin@example.com",
                    username="admin",
                    hashed_password=get_password_hash("admin123"),
                    is_active=True,
                    is_superuser=True
                )
                db.add(admin)
                db.commit()
                logger.info("✅ Usuário admin criado com sucesso!")
                logger.info("   Email: admin@example.com")
                logger.info("   Senha: admin123")
                logger.info("   ⚠️  IMPORTANTE: Altere a senha em produção!")
            else:
                logger.info("✓ Usuário admin já existe")
        finally:
            db.close()

    except Exception as e:
        logger.error(f"❌ Erro ao configurar usuário admin: {e}")
        # Não falhar o setup se o admin não puder ser criado
        # (pode ser que o banco ainda não esteja pronto)

if __name__ == "__main__":
    setup_database()
