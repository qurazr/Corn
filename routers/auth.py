"""
Aevi - Authentication Router
Файл: app/routers/auth.py
Вход через Telegram WebApp, JWT токены
"""

import hashlib
import hmac
import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import jwt

from app.config import settings
from app.database.session import get_db
from app.database.models import User

router = APIRouter()
security = HTTPBearer()

# Модели запросов/ответов
class InitDataRequest(BaseModel):
    init_data: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    is_new_user: bool

class UserInfoResponse(BaseModel):
    id: int
    tg_id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    xp: int
    level: int
    coins: int
    streak: int
    current_language: str


def verify_telegram_init_data(init_data: str) -> dict:
    """
    Проверяет подпись Telegram WebApp initData
    Документация: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    """
    if not init_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No init data provided"
        )
    
    # Парсим параметры
    params = {}
    for pair in init_data.split("&"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            params[key] = value
    
    # Получаем хеш
    received_hash = params.pop("hash", None)
    if not received_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No hash in init data"
        )
    
    # Сортируем ключи и формируем строку для проверки
    sorted_keys = sorted(params.keys())
    check_string = "\n".join(f"{k}={params[k]}" for k in sorted_keys)
    
    # Генерируем секретный ключ из токена бота
    secret_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()
    
    # Вычисляем ожидаемый хеш
    computed_hash = hmac.new(
        secret_key, 
        check_string.encode(), 
        hashlib.sha256
    ).hexdigest()
    
    # Сравниваем
    if computed_hash != received_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid hash"
        )
    
    # Проверяем, что данные не устарели (максимум 24 часа)
    if "auth_date" in params:
        auth_date = int(params["auth_date"])
        current_time = int(datetime.now().timestamp())
        if current_time - auth_date > 86400:  # 24 часа
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Auth data expired"
            )
    
    return params


def decode_user_from_init_data(init_data: str) -> dict:
    """Извлекает данные пользователя из валидного initData"""
    params = verify_telegram_init_data(init_data)
    
    if "user" not in params:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user data in init data"
        )
    
    user_data = json.loads(params["user"])
    return user_data


def create_access_token(user_id: int) -> str:
    """Создаёт JWT токен для пользователя"""
    expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> int:
    """Декодирует JWT и возвращает user_id"""
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return int(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Dependency для получения текущего пользователя по JWT"""
    token = credentials.credentials
    user_id = decode_access_token(token)
    
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post("/auth/telegram", response_model=AuthResponse)
async def auth_via_telegram(
    request: InitDataRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентификация через Telegram WebApp
    Принимает initData, возвращает JWT токен
    """
    # Валидируем и получаем данные пользователя из Telegram
    user_data = decode_user_from_init_data(request.init_data)
    
    tg_id = user_data.get("id")
    username = user_data.get("username")
    first_name = user_data.get("first_name", "")
    last_name = user_data.get("last_name")
    
    if not tg_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user ID in Telegram data"
        )
    
    # Ищем пользователя в БД
    result = await db.execute(
        select(User).where(User.tg_id == tg_id)
    )
    user = result.scalar_one_or_none()
    
    is_new_user = False
    
    if not user:
        # Создаём нового пользователя
        user = User(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            registered_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        is_new_user = True
    else:
        # Обновляем last_active
        user.last_active = datetime.utcnow()
        if username and user.username != username:
            user.username = username
        await db.commit()
    
    # Создаём JWT токен
    access_token = create_access_token(user.id)
    
    return AuthResponse(
        access_token=access_token,
        user_id=user.id,
        is_new_user=is_new_user
    )


@router.get("/auth/me", response_model=UserInfoResponse)
async def get_my_info(
    current_user: User = Depends(get_current_user)
):
    """Получить информацию о текущем пользователе"""
    return UserInfoResponse(
        id=current_user.id,
        tg_id=current_user.tg_id,
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        xp=current_user.xp,
        level=current_user.level,
        coins=current_user.coins,
        streak=current_user.streak,
        current_language=current_user.current_language
    )


@router.post("/auth/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Логаут (на клиенте нужно удалить токен)
    Сервер просто возвращает успех
    """
    return {"message": "Logged out successfully"}


@router.post("/auth/refresh")
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """Обновить JWT токен"""
    new_token = create_access_token(current_user.id)
    return {"access_token": new_token, "token_type": "bearer"}