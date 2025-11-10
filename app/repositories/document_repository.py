from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.document import Document
from app.schemas.document import DocumentCreate

class DocumentRepository:
    """
    Repository para operações de Document

    Responsabilidades:
    - CRUD de documentos
    - Queries específicas de documentos
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, document_id: int) -> Optional[Document]:
        """Busca documento por ID"""
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_by_owner(self, owner_id: int, skip: int = 0, limit: int = 100) -> List[Document]:
        """Busca documentos por proprietário"""
        return (
            self.db.query(Document)
            .filter(Document.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, document_data: DocumentCreate) -> Document:
        """Cria novo documento"""
        db_document = Document(**document_data.model_dump())
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def update(self, document: Document) -> Document:
        """Atualiza documento"""
        self.db.commit()
        self.db.refresh(document)
        return document

    def delete(self, document: Document) -> None:
        """Deleta documento"""
        self.db.delete(document)
        self.db.commit()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """Lista todos os documentos"""
        return self.db.query(Document).offset(skip).limit(limit).all()
