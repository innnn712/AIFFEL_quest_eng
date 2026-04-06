# app/middleware.py
"""
Day 3 - 요청 로깅 미들웨어
"""
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.logger_config import setup_logger

logger = setup_logger("middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """모든 요청/응답을 로깅하는 미들웨어."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        elapsed = round(time.time() - start_time, 3)
        logger.info(
            f"{request.method} {request.url.path} "
            f"→ {response.status_code} ({elapsed}s)"
        )

        return response