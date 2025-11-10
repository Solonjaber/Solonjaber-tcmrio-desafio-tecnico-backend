from pydantic import BaseModel, Field
from typing import List, Optional

class SearchQuery(BaseModel):
    """Schema para query de busca semântica"""
    query: str = Field(..., min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=50)
    document_ids: Optional[List[int]] = None  # Filtrar por documentos específicos

class SearchResult(BaseModel):
    """Schema para resultado individual de busca"""
    document_id: int
    document_name: str
    chunk_text: str
    similarity_score: float
    chunk_index: int

class SearchResponse(BaseModel):
    """Schema para resposta de busca"""
    query: str
    results: List[SearchResult]
    total_results: int

class ChatQuery(BaseModel):
    """Schema para perguntas ao LLM sobre documentos"""
    query: str = Field(..., min_length=1, max_length=1000)
    document_ids: Optional[List[int]] = None
    use_context: bool = True  # Usar busca semântica como contexto
    max_context_chunks: int = Field(default=3, ge=1, le=10)

class ChatResponse(BaseModel):
    """Schema para resposta do chat"""
    query: str
    answer: str
    context_used: List[SearchResult]
    llm_provider: str  # Renomeado de model_used para evitar conflito com namespace protegido do Pydantic
