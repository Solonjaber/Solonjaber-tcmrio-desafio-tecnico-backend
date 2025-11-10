from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.search import ChatQuery, ChatResponse
from app.services.llm_service import LLMService
from app.services.vector_service import VectorService
from app.repositories.vector_repository import VectorRepository

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_documents(
    chat_query: ChatQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat com LLM usando contexto dos documentos

    Combina busca semântica + LLM para responder perguntas
    sobre os documentos de forma natural.

    - **query**: Pergunta para o LLM
    - **document_ids**: (Opcional) Filtrar documentos
    - **use_context**: Se deve buscar contexto nos documentos
    - **max_context_chunks**: Quantos chunks usar como contexto
    """
    try:
        context_chunks = []

        # 1. Buscar contexto se necessário
        if chat_query.use_context:
            vector_service = VectorService()
            vector_repo = VectorRepository(db)

            context_chunks = vector_service.search(
                query=chat_query.query,
                vector_repo=vector_repo,
                top_k=chat_query.max_context_chunks,
                document_ids=chat_query.document_ids,
                user_id=current_user.id
            )

        # 2. Gerar resposta com LLM
        llm_service = LLMService()
        answer = await llm_service.generate_answer(
            query=chat_query.query,
            context_chunks=context_chunks
        )

        return ChatResponse(
            query=chat_query.query,
            answer=answer,
            context_used=context_chunks,
            llm_provider=llm_service.provider
        )

    except NotImplementedError as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=(
                "🔧 LLM não configurado. "
                "Configure OPENAI_API_KEY, AZURE_OPENAI_API_KEY ou OLLAMA_BASE_URL no .env "
                "e implemente o método correspondente em llm_service.py"
            )
        )
