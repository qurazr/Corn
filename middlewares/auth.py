"""
Aevi - Authentication Middleware
Файл: app/middlewares/auth.py
Проверяет JWT для защищённых эндпоинтов
"""

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
import re

from app.config import settings

# Список публичных эндпоинтов (не требуют авторизации)
PUBLIC_PATHS = [
    r"^/$",
    r"^/health$",
    r"^/api/docs",
    r"^/api/redoc",
    r"^/openapi.json",
    r"^/api/auth/telegram$",  # вход
    r"^/api/auth/refresh$",   # обновление токена (требует валидный токен, но проверяем в самом хендлере)
]

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Мидлварь для проверки JWT токена
    Пропускает публичные эндпоинты без проверки
    """
    
    def is_public_path(self, path: str) -> bool:
        """Проверяет, является ли путь публичным"""
        for pattern in PUBLIC_PATHS:
            if re.match(pattern, path):
                return True
        return False
    
    async def dispatch(self, request: Request, call_next):
        # Пропускаем публичные пути
        if self.is_public_path(request.url.path):
            return await call_next(request)
        
        # Для остальных — проверяем наличие и валидность токена
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing authorization header"
            )
        
        # Формат: "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format. Use: Bearer <token>"
            )
        
        token = parts[1]
        
        # Валидируем токен (делегируем проверку в auth модуль)
        try:
            from app.routers.auth import decode_access_token
            user_id = decode_access_token(token)
            # Добавляем user_id в request state для использования в хендлерах
            request.state.user_id = user_id
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return await call_next(request)