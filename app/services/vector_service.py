from sentence_transformers import SentenceTransformer
from typing import List
from app.core.config import settings
from app.repositories.vector_repository import VectorRepository
from app.schemas.search import SearchResult
import numpy as np

class VectorService:
    """
    Service para vetorização e busca

    Responsabilidades:
    - Gerar embeddings de texto
    - Realizar busca semântica
    - Gerenciar modelo de embedding
    """

    def __init__(self):
        # Carregar modelo de embedding
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Gera embeddings para lista de textos"""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def search(
        self,
        query: str,
        vector_repo: VectorRepository,
        top_k: int = 5,
        document_ids: List[int] = None,
        user_id: int = None
    ) -> List[SearchResult]:
        """
        Realiza busca semântica
        """
        # Gerar embedding da query
        query_embedding = self.generate_embeddings([query])[0]

        # Buscar no banco
        results = vector_repo.similarity_search(
            query_embedding,
            top_k=top_k,
            document_ids=document_ids,
            user_id=user_id
        )

        # Converter para SearchResult
        search_results = []
        for vector, document, similarity in results:
            search_results.append(SearchResult(
                document_id=document.id,
                document_name=document.original_filename,
                chunk_text=vector.chunk_text,
                similarity_score=float(similarity),
                chunk_index=vector.chunk_index
            ))

        return search_results
