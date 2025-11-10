from fastapi import Request
import time
from app.core.logging import logger
import uuid

async def logging_middleware(request: Request, call_next):
    """
    Middleware para logging de requisições

    Responsabilidades:
    - Log de cada requisição
    - Medir tempo de resposta
    - Adicionar request_id
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    logger.info(
        f"Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else None
        }
    )

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"Request completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": round(process_time, 3)
        }
    )

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(round(process_time, 3))

    return response
