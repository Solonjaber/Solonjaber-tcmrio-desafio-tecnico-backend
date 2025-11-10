from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.search import SearchQuery, SearchResponse
from app.services.vector_service import VectorService
from app.repositories.vector_repository import VectorRepository

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=SearchResponse)
async def semantic_search(
    search_query: SearchQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca semântica nos documentos

    Realiza busca vetorial usando embeddings para encontrar
    os trechos mais relevantes baseado na query.

    - **query**: Texto da pergunta/busca
    - **top_k**: Número de resultados a retornar (1-50)
    - **document_ids**: (Opcional) Filtrar por documentos específicos
    """
    vector_service = VectorService()
    vector_repo = VectorRepository(db)

    results = vector_service.search(
        query=search_query.query,
        vector_repo=vector_repo,
        top_k=search_query.top_k,
        document_ids=search_query.document_ids,
        user_id=current_user.id
    )

    return SearchResponse(
        query=search_query.query,
        results=results,
        total_results=len(results)
    )
