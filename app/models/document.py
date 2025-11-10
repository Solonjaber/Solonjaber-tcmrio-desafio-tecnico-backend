from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Document(Base):
    """
    Modelo de documento

    Responsabilidades:
    - Armazenar metadados do documento
    - Relacionar com usuário proprietário
    - Relacionar com vetores extraídos
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(BigInteger)  # em bytes
    file_type = Column(String)  # pdf, docx
    content_text = Column(Text)  # texto extraído completo

    # Metadados
    page_count = Column(Integer)
    word_count = Column(Integer)

    # Relacionamentos
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="documents")

    vectors = relationship(
        "VectorStore",
        back_populates="document",
        cascade="all, delete-orphan"
    )

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename})>"
