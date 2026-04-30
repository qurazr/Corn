"""
Aevi - User Profile Router
Файл: app/routers/user.py
Управление профилем, настройками, смена языка
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel, Field
from typing import Optional

from app.database.session import get_db
from app.database.models import User, Language
from app.routers.auth import get_current_user

router = APIRouter()

# Модели запросов
class UpdateProfileRequest(BaseModel):
    username: Optional[str] = Field(None, max_length=64)
    daily_goal: Optional[int] = Field(None, ge=5, le=100)
    theme: Optional[str] = Field(None, pattern="^(neon|dark|light)$")
    notifications_enabled: Optional[bool] = None

class ChangeLanguageRequest(BaseModel):
    language_code: str = Field(..., min_length=2, max_length=10)

class UserStatsResponse(BaseModel):
    xp: int
    level: int
    xp_to_next_level: int
    coins: int
    streak: int
    total_words_learned: int
    total_lessons_completed: int
    total_time_spent: int  # минут
    rank: Optional[int] = None


def calculate_level(xp: int) -> tuple[int, int]:
    """Расчёт уровня и XP до следующего уровня"""
    # Формула: (level * 100) + (level-1 * 50)
    level = 1
    xp_needed = 100
    
    while xp >= xp_needed:
        xp -= xp_needed
        level += 1
        xp_needed = 100 + (level - 1) * 50
    
    return level, xp_needed - xp


@router.get("/user/profile")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """Получить полный профиль пользователя"""
    return {
        "id": current_user.id,
        "tg_id": current_user.tg_id,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "xp": current_user.xp,
        "level": current_user.level,
        "coins": current_user.coins,
        "streak": current_user.streak,
        "total_words_learned": current_user.total_words_learned,
        "total_lessons_completed": current_user.total_lessons_completed,
        "current_language": current_user.current_language,
        "daily_goal": current_user.daily_goal,
        "theme": current_user.theme,
        "notifications_enabled": current_user.notifications_enabled,
        "registered_at": current_user.registered_at.isoformat(),
        "last_active": current_user.last_active.isoformat()
    }


@router.patch("/user/profile")
async def update_profile(
    update_data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить настройки профиля"""
    if update_data.username is not None:
        current_user.username = update_data.username
    
    if update_data.daily_goal is not None:
        current_user.daily_goal = update_data.daily_goal
    
    if update_data.theme is not None:
        current_user.theme = update_data.theme
    
    if update_data.notifications_enabled is not None:
        current_user.notifications_enabled = update_data.notifications_enabled
    
    await db.commit()
    await db.refresh(current_user)
    
    return {"message": "Profile updated successfully"}


@router.post("/user/change-language")
async def change_language(
    request: ChangeLanguageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Сменить основной язык для изучения"""
    # Проверяем, существует ли такой язык
    result = await db.execute(
        select(Language).where(Language.code == request.language_code)
    )
    language = result.scalar_one_or_none()
    
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language {request.language_code} not found"
        )
    
    current_user.current_language = request.language_code
    await db.commit()
    
    return {
        "message": f"Language changed to {language.name}",
        "language_code": request.language_code,
        "language_name": language.name
    }


@router.get("/user/stats", response_model=UserStatsResponse)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить расширенную статистику пользователя"""
    level, xp_to_next = calculate_level(current_user.xp)
    
    # TODO: получить ранг из таблицы лидеров
    rank = None
    
    return UserStatsResponse(
        xp=current_user.xp,
        level=level,
        xp_to_next_level=xp_to_next,
        coins=current_user.coins,
        streak=current_user.streak,
        total_words_learned=current_user.total_words_learned,
        total_lessons_completed=current_user.total_lessons_completed,
        total_time_spent=current_user.total_time_spent,
        rank=rank
    )


@router.get("/user/available-languages")
async def get_available_languages(
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех доступных языков"""
    result = await db.execute(
        select(Language).where(Language.is_active == True)
    )
    languages = result.scalars().all()
    
    return [
        {
            "code": lang.code,
            "name": lang.name,
            "flag": lang.flag
        }
        for lang in languages
    ]


@router.post("/user/update-streak")
async def update_streak(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить ежедневную серию (вызывается при активности)"""
    from datetime import datetime, timedelta
    
    now = datetime.utcnow()
    last_active = current_user.last_active
    
    # Если последняя активность была вчера — увеличиваем streak
    if last_active.date() == (now - timedelta(days=1)).date():
        current_user.streak += 1
    # Если сегодня — ничего не меняем
    elif last_active.date() != now.date():
        # Пропустил день — сбрасываем streak
        current_user.streak = 1
    
    current_user.last_active = now
    await db.commit()
    
    return {
        "streak": current_user.streak,
        "message": "Streak updated"
    }