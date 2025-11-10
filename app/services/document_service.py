import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.repositories.vector_repository import VectorRepository
from app.schemas.document import DocumentCreate
from app.utils.file_validator import FileValidator
from app.utils.text_extractor import TextExtractor
from app.utils.text_chunker import TextChunker
from app.services.vector_service import VectorService
from app.core.config import settings
from app.core.exceptions import FileUploadError, NotFoundError
from app.core.logging import logger

class DocumentService:
    """
    Service para gestão de documentos

    Responsabilidades:
    - Upload de documentos
    - Processamento (extração, chunking, vetorização)
    - Gestão de documentos
    """

    def __init__(self, db: Session):
        self.db = db
        self.doc_repo = DocumentRepository(db)
        self.vector_repo = VectorRepository(db)
        self.vector_service = VectorService()

    async def upload_document(
        self,
        file: UploadFile,
        user_id: int
    ) -> Document:
        """
        Processa upload completo de documento
        1. Valida arquivo
        2. Salva no disco
        3. Extrai texto
        4. Divide em chunks
        5. Vetoriza
        6. Salva no banco
        """
        try:
            # 1. Validar arquivo
            extension, original_filename = FileValidator.validate_file(file)
            safe_filename = FileValidator.generate_safe_filename(
                original_filename, user_id
            )

            # 2. Criar diretório se não existir
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

            # 3. Salvar arquivo
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            file_size = os.path.getsize(file_path)

            logger.info(f"Arquivo salvo: {file_path}")

            # 4. Extrair texto
            text_content, page_count, word_count = TextExtractor.extract_text(
                file_path, extension
            )

            logger.info(f"Texto extraído: {word_count} palavras, {page_count} páginas")

            # 5. Dividir em chunks
            chunks = TextChunker.chunk_text(text_content)
            logger.info(f"Documento dividido em {len(chunks)} chunks")

            # 6. Criar documento no banco
            document_data = DocumentCreate(
                filename=safe_filename,
                original_filename=original_filename,
                file_path=file_path,
                file_size=file_size,
                file_type=extension,
                content_text=text_content,
                page_count=page_count,
                word_count=word_count,
                owner_id=user_id
            )

            document = self.doc_repo.create(document_data)
            logger.info(f"Documento criado no banco: ID {document.id}")

            # 7. Gerar embeddings
            embeddings = self.vector_service.generate_embeddings(chunks)
            logger.info(f"Embeddings gerados para {len(embeddings)} chunks")

            # 8. Salvar vetores no banco
            self.vector_repo.create_batch(document.id, chunks, embeddings)
            logger.info(f"Vetores salvos no banco")

            # 🔧 VOCÊ INTEGRA: Notificar N8n sobre novo documento
            # await self._notify_n8n(document, user_id)

            return document

        except Exception as e:
            # Limpar arquivo se houver erro
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            logger.error(f"Erro no upload: {str(e)}")
            raise FileUploadError(f"Erro ao processar arquivo: {str(e)}")

    async def _notify_n8n(self, document: Document, user_id: int):
        """
        🔧 VOCÊ INTEGRA: Envia notificação para N8n quando documento é criado

        PASSOS PARA INTEGRAR:
        1. Criar workflow no N8n com webhook trigger
        2. Configurar no .env: N8N_WEBHOOK_URL=http://localhost:5678/webhook/document-upload
        3. Descomentar a linha 102 no método upload_document()

        EXEMPLO DE IMPLEMENTAÇÃO:
        ```python
        import httpx

        if not settings.N8N_WEBHOOK_URL:
            logger.warning("N8N_WEBHOOK_URL não configurado, pulando notificação")
            return

        try:
            payload = {
                "event": "document_uploaded",
                "timestamp": document.created_at.isoformat(),
                "document": {
                    "id": document.id,
                    "filename": document.original_filename,
                    "file_type": document.file_type,
                    "file_size": document.file_size,
                    "page_count": document.page_count,
                    "word_count": document.word_count,
                },
                "user_id": user_id
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    settings.N8N_WEBHOOK_URL,
                    json=payload
                )
                response.raise_for_status()
                logger.info(f"Notificação N8n enviada para documento {document.id}")

        except httpx.HTTPError as e:
            logger.error(f"Erro ao notificar N8n: {e}")
            # Não falhar o upload se notificação falhar
        except Exception as e:
            logger.error(f"Erro inesperado ao notificar N8n: {e}")
        ```

        EXEMPLO DE WORKFLOW N8n:
        1. Webhook Node (trigger)
        2. Function Node (processar dados)
        3. Email/Slack/Discord Node (notificar equipe)

        DOCUMENTAÇÃO: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
        """
        pass  # Implementar seguindo o exemplo acima

    def get_document(self, document_id: int, user_id: int) -> Document:
        """Busca documento com verificação de permissão"""
        document = self.doc_repo.get_by_id(document_id)

        if not document:
            raise NotFoundError("Documento não encontrado")

        if document.owner_id != user_id:
            raise NotFoundError("Documento não encontrado")

        return document

    def list_documents(self, user_id: int, skip: int = 0, limit: int = 100):
        """Lista documentos do usuário"""
        return self.doc_repo.get_by_owner(user_id, skip, limit)

    def delete_document(self, document_id: int, user_id: int):
        """Deleta documento e seus vetores"""
        document = self.get_document(document_id, user_id)

        # Deletar arquivo físico
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Deletar do banco (cascade deleta os vetores)
        self.doc_repo.delete(document)

        logger.info(f"Documento {document_id} deletado")
