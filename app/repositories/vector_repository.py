from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from app.models.vector_store import VectorStore
from app.models.document import Document
import numpy as np

class VectorRepository:
    """
    Repository para operações vetoriais

    Responsabilidades:
    - CRUD de vetores
    - Busca por similaridade
    """

    def __init__(self, db: Session):
        self.db = db

    def create_batch(
        self,
        document_id: int,
        chunks: List[str],
        embeddings: List[List[float]]
    ) -> List[VectorStore]:
        """Cria múltiplos vetores de uma vez"""
        vectors = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector = VectorStore(
                document_id=document_id,
                chunk_text=chunk,
                chunk_index=idx,
                embedding=embedding
            )
            vectors.append(vector)

        self.db.add_all(vectors)
        self.db.commit()
        return vectors

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_ids: Optional[List[int]] = None,
        user_id: Optional[int] = None
    ) -> List[tuple]:
        """
        Busca por similaridade vetorial usando pgvector
        Retorna: List[(VectorStore, Document, similarity_score)]
        """
        # Converter query para o formato do pgvector
        query_vector = np.array(query_embedding)

        # Query base com join no documento
        query = (
            select(
                VectorStore,
                Document,
                VectorStore.embedding.cosine_distance(query_vector).label("distance")
            )
            .join(Document, VectorStore.document_id == Document.id)
        )

        # Filtrar por usuário (IMPORTANTE: segurança)
        if user_id is not None:
            query = query.where(Document.owner_id == user_id)

        # Filtrar por documentos específicos se fornecido
        if document_ids:
            query = query.where(VectorStore.document_id.in_(document_ids))

        # Ordenar por similaridade e limitar resultados
        query = query.order_by("distance").limit(top_k)

        results = self.db.execute(query).all()

        # Converter distância para similaridade (1 - distance)
        return [
            (vector, doc, 1 - distance)
            for vector, doc, distance in results
        ]

    def get_by_document(self, document_id: int) -> List[VectorStore]:
        """Busca todos os vetores de um documento"""
        return (
            self.db.query(VectorStore)
            .filter(VectorStore.document_id == document_id)
            .order_by(VectorStore.chunk_index)
            .all()
        )

    def delete_by_document(self, document_id: int) -> None:
        """Deleta todos os vetores de um documento"""
        self.db.query(VectorStore).filter(
            VectorStore.document_id == document_id
        ).delete()
        self.db.commit()

    def count_by_document(self, document_id: int) -> int:
        """Conta quantos chunks um documento tem"""
        return (
            self.db.query(func.count(VectorStore.id))
            .filter(VectorStore.document_id == document_id)
            .scalar()
        )
