import os
from typing import Tuple
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import FileUploadError

class FileValidator:
    """
    Valida arquivos antes do upload

    Responsabilidades:
    - Validar extensão do arquivo
    - Validar tamanho do arquivo
    - Gerar nome seguro para o arquivo
    """

    @staticmethod
    def validate_file(file: UploadFile) -> Tuple[str, str]:
        """
        Valida arquivo e retorna (extensão, nome_seguro)
        """
        # Validar extensão
        filename = file.filename or ""
        extension = filename.split(".")[-1].lower()

        if extension not in settings.allowed_extensions_list:
            raise FileUploadError(
                f"Extensão .{extension} não permitida. "
                f"Permitidas: {', '.join(settings.allowed_extensions_list)}"
            )

        # Validar tamanho (se disponível)
        if hasattr(file, 'size') and file.size:
            max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
            if file.size > max_size:
                raise FileUploadError(
                    f"Arquivo muito grande. Máximo: {settings.MAX_FILE_SIZE_MB}MB"
                )

        return extension, filename

    @staticmethod
    def generate_safe_filename(original_filename: str, user_id: int) -> str:
        """Gera nome de arquivo seguro e único"""
        import uuid
        from datetime import datetime

        extension = original_filename.split(".")[-1]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]

        return f"user_{user_id}_{timestamp}_{unique_id}.{extension}"
