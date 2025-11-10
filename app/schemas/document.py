from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DocumentUpload(BaseModel):
    """Schema para upload de documento"""
    # O arquivo vem no FormData, não no body JSON
    pass

class DocumentBase(BaseModel):
    """Schema base para documento"""
    filename: str
    file_type: str

class DocumentCreate(DocumentBase):
    """Schema para criação de documento"""
    original_filename: str
    file_path: str
    file_size: int
    content_text: str
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    owner_id: int

class DocumentResponse(BaseModel):
    """Schema para resposta de documento"""
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    page_count: Optional[int]
    word_count: Optional[int]
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class DocumentDetail(DocumentResponse):
    """Schema detalhado de documento"""
    content_text: Optional[str] = None
    chunk_count: Optional[int] = None
