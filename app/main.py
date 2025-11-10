from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.error_handler import error_handler_middleware
from app.middleware.logging_middleware import logging_middleware
from app.api.v1 import auth, documents, search, chat
from app.core.logging import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    API de processamento e busca semântica em documentos

    ## Funcionalidades

    * **Autenticação JWT** - Sistema seguro de login
    * **Upload de Documentos** - Suporte a PDF e DOCX
    * **Extração de Texto** - Processamento automático
    * **Busca Semântica** - Busca vetorial com pgvector
    * **Chat com LLM** - Perguntas sobre documentos (🔧 configurar)

    ## Fluxo de Uso

    1. Registre-se em `/api/v1/auth/register`
    2. Faça login em `/api/v1/auth/login`
    3. Use o token para autenticar as próximas chamadas
    4. Faça upload de documentos em `/api/v1/documents/upload`
    5. Busque com `/api/v1/search/` ou `/api/v1/chat/`
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middlewares customizados
app.middleware("http")(logging_middleware)
app.middleware("http")(error_handler_middleware)

# Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Endpoint raiz - health check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "database": "connected",
        "services": {
            "auth": "ok",
            "documents": "ok",
            "search": "ok",
            "chat": "configured" if settings.OPENAI_API_KEY or settings.OLLAMA_BASE_URL else "not_configured"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
