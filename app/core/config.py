from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application
    APP_NAME: str = "Document AI API"
    APP_VERSION: str = "1.0.0"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: str = "pdf,docx"  # Comma-separated file extensions

    @property
    def allowed_extensions_list(self) -> List[str]:
        """
        Retorna ALLOWED_EXTENSIONS como lista.
        Aceita string separada por vírgula no .env para simplicidade,
        mas expõe como lista para type safety no código.
        """
        if isinstance(self.ALLOWED_EXTENSIONS, list):
            return self.ALLOWED_EXTENSIONS
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(',')]

    # Vector
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_DIMENSION: int = 384

    # LLM Settings
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    AZURE_OPENAI_ENDPOINT: str | None = None
    AZURE_OPENAI_API_KEY: str | None = None
    AZURE_OPENAI_DEPLOYMENT: str | None = None

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"

    # N8n Integration
    N8N_WEBHOOK_URL: str | None = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
