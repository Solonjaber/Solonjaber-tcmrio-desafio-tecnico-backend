from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.document import DocumentResponse, DocumentDetail
from app.services.document_service import DocumentService
from app.core.exceptions import FileUploadError, NotFoundError
from app.repositories.vector_repository import VectorRepository

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload de documento (PDF ou DOCX)

    O documento será:
    1. Validado
    2. Salvo no servidor
    3. Processado (extração de texto)
    4. Vetorizado para busca semântica

    - **file**: Arquivo PDF ou DOCX (máximo 10MB)
    """
    try:
        doc_service = DocumentService(db)
        document = await doc_service.upload_document(file, current_user.id)
        return document
    except FileUploadError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista documentos do usuário autenticado

    - **skip**: Número de documentos para pular (paginação)
    - **limit**: Número máximo de documentos a retornar
    """
    doc_service = DocumentService(db)
    return doc_service.list_documents(current_user.id, skip, limit)

@router.get("/{document_id}", response_model=DocumentDetail)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca documento específico com detalhes completos

    - **document_id**: ID do documento
    """
    try:
        doc_service = DocumentService(db)
        document = doc_service.get_document(document_id, current_user.id)

        # Adicionar contagem de chunks
        vector_repo = VectorRepository(db)
        chunk_count = vector_repo.count_by_document(document_id)

        # Converter para DocumentDetail
        doc_dict = {
            "id": document.id,
            "filename": document.filename,
            "original_filename": document.original_filename,
            "file_type": document.file_type,
            "file_size": document.file_size,
            "page_count": document.page_count,
            "word_count": document.word_count,
            "created_at": document.created_at,
            "owner_id": document.owner_id,
            "content_text": document.content_text[:500] + "...",  # Truncar
            "chunk_count": chunk_count
        }

        return doc_dict
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deleta documento e seus vetores

    - **document_id**: ID do documento
    """
    try:
        doc_service = DocumentService(db)
        doc_service.delete_document(document_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
