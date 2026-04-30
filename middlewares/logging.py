"""
Aevi - Logging Middleware
Файл: app/middlewares/logging.py
"""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("aevi.http")

class LoggingMiddleware(BaseHTTPMiddleware):
    """Логирование всех HTTP запросов"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Логируем входящий запрос
        logger.info(f"→ {request.method} {request.url.path}")
        
        # Обрабатываем запрос
        response = await call_next(request)
        
        # Считаем время выполнения
        process_time = time.time() - start_time
        
        # Логируем ответ
        logger.info(
            f"← {request.method} {request.url.path} → {response.status_code} "
            f"({process_time:.3f}s)"
        )
        
        # Добавляем заголовок с временем выполнения
        response.headers["X-Process-Time"] = str(process_time)
        
        return response