from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.database import Base
from app.core.config import settings

class VectorStore(Base):
    """
    Modelo de armazenamento vetorial com pgvector

    Responsabilidades:
    - Armazenar embeddings dos chunks de texto
    - Permitir busca por similaridade vetorial
    - Relacionar chunks com documento original
    """
    __tablename__ = "vector_store"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    # Conteúdo
    chunk_text = Column(Text, nullable=False)  # texto do chunk
    chunk_index = Column(Integer)  # ordem do chunk no documento

    # Vector embedding (pgvector)
    embedding = Column(Vector(settings.VECTOR_DIMENSION))

    # Metadados do chunk
    chunk_metadata = Column(Text)  # JSON string com metadados adicionais

    # Relacionamento
    document = relationship("Document", back_populates="vectors")

    def __repr__(self):
        return f"<VectorStore(id={self.id}, document_id={self.document_id})>"
