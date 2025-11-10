from fastapi import HTTPException, status

class DocumentAIException(Exception):
    """Base exception para a aplicação"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(DocumentAIException):
    """Erro de autenticação"""
    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class AuthorizationError(DocumentAIException):
    """Erro de autorização"""
    def __init__(self, message: str = "Sem permissão"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)

class NotFoundError(DocumentAIException):
    """Recurso não encontrado"""
    def __init__(self, message: str = "Recurso não encontrado"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class ValidationError(DocumentAIException):
    """Erro de validação"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)

class FileUploadError(DocumentAIException):
    """Erro no upload de arquivo"""
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
