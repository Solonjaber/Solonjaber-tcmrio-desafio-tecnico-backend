from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import DocumentAIException
from app.core.logging import logger
import traceback

async def error_handler_middleware(request: Request, call_next):
    """
    Middleware para tratamento global de erros

    Responsabilidades:
    - Capturar exceções não tratadas
    - Log estruturado de erros
    - Resposta padronizada
    """
    try:
        return await call_next(request)

    except DocumentAIException as e:
        logger.error(
            f"DocumentAIException: {e.message}",
            extra={
                "status_code": e.status_code,
                "path": request.url.path
            }
        )
        return JSONResponse(
            status_code=e.status_code,
            content={
                "error": e.message,
                "type": type(e).__name__
            }
        )

    except Exception as e:
        logger.error(
            f"Unhandled exception: {str(e)}",
            extra={
                "path": request.url.path,
                "traceback": traceback.format_exc()
            }
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Erro interno do servidor",
                "type": "InternalServerError"
            }
        )
