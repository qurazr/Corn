"""
Aevi - Statistics Router
Файл: app/routers/stats.py
Статистика, графики, достижения, тепловая карта, лидерборд
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc, case
from datetime import datetime, timedelta, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import calendar

from app.database.session import get_db
from app.database.models import (
    User, Word, Language, UserWordProgress, 
    Achievement, user_achievements_table, UserDailyTask
)
from app.routers.auth import get_current_user
from app.routers.learning import calculate_level

router = APIRouter()

# Модели ответов
class StreakDay(BaseModel):
    date: str
    studied: bool
    words_learned: int

class HeatmapResponse(BaseModel):
    year: int
    months: List[Dict[str, Any]]
    streak_days: List[StreakDay]
    longest_streak: int
    current_streak: int

class LeaderboardUser(BaseModel):
    rank: int
    user_id: int
    username: Optional[str]
    first_name: str
    xp: int
    level: int
    words_learned: int
    avatar_color: str = "#8b5cf6"

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    earned: bool
    earned_at: Optional[str]
    progress: Optional[int]  # прогресс в % к получению
    progress_current: Optional[int]
    progress_target: Optional[int]

class LanguageProgress(BaseModel):
    language_code: str
    language_name: str
    flag: str
    words_learned: int
    level_progress: int  # % прогресса по языку
    current_level: str

class WeeklyActivity(BaseModel):
    day: str
    words: int
    xp: int


@router.get("/stats/heatmap")
async def get_learning_heatmap(
    year: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Тепловая карта активности (календарь занятий)
    Возвращает данные за год или за текущий год
    """
    if year is None:
        year = datetime.utcnow().year
    
    # Получаем статистику по дням за год
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    
    # Группируем прогресс по дням
    result = await db.execute(
        select(
            func.date(UserWordProgress.last_practiced).label("study_date"),
            func.count(UserWordProgress.id).label("words_count")
        )
        .where(UserWordProgress.user_id == current_user.id)
        .where(func.date(UserWordProgress.last_practiced) >= start_date)
        .where(func.date(UserWordProgress.last_practiced) <= end_date)
        .group_by(func.date(UserWordProgress.last_practiced))
    )
    
    daily_stats = {row.study_date: row.words_count for row in result.fetchall()}
    
    # Формируем тепловую карту по месяцам
    months_data = []
    streak_days = []
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    today = date.today()
    
    for month in range(1, 13):
        month_days = calendar.monthrange(year, month)[1]
        days = []
        
        for day in range(1, month_days + 1):
            current_date = date(year, month, day)
            date_str = current_date.isoformat()
            words = daily_stats.get(date_str, 0)
            studied = words > 0
            
            days.append({
                "day": day,
                "studied": studied,
                "words": words
            })
            
            # Расчёт streak
            if studied:
                temp_streak += 1
                if temp_streak > longest_streak:
                    longest_streak = temp_streak
                
                # Проверяем, является ли этот день частью текущей серии
                if current_date == today or (
                    current_streak == 0 and 
                    current_date == today - timedelta(days=temp_streak - 1)
                ):
                    current_streak = temp_streak
            else:
                temp_streak = 0
            
            streak_days.append(StreakDay(
                date=date_str,
                studied=studied,
                words_learned=words
            ))
        
        months_data.append({
            "month": month,
            "month_name": calendar.month_name[month],
            "days": days
        })
    
    return HeatmapResponse(
        year=year,
        months=months_data,
        streak_days=streak_days,
        longest_streak=longest_streak,
        current_streak=current_streak
    )


@router.get("/stats/leaderboard")
async def get_leaderboard(
    period: str = "all_time",  # daily, weekly, monthly, all_time
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Таблица лидеров
    Периоды: daily, weekly, monthly, all_time
    """
    now = datetime.utcnow()
    
    # Определяем временные рамки
    if period == "daily":
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "monthly":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = None
    
    # Запрос пользователей с сортировкой по XP
    query = select(User)
    
    if start_date:
        # Для периода считаем XP, полученный за период
        query = query.join(UserWordProgress).where(
            UserWordProgress.user_id == User.id,
            UserWordProgress.last_practiced >= start_date
        ).group_by(User.id).order_by(
            desc(func.sum(UserWordProgress.times_correct * 10))
        )
    else:
        query = query.order_by(desc(User.xp))
    
    query = query.limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    
    # Получаем текущего пользователя для определения его ранга
    current_user_rank_query = select(func.count(User.id)).where(User.xp > current_user.xp)
    current_rank_result = await db.execute(current_user_rank_query)
    current_user_rank = (current_rank_result.scalar() or 0) + 1
    
    leaderboard = []
    for idx, user in enumerate(users, 1):
        leaderboard.append(LeaderboardUser(
            rank=idx,
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            xp=user.xp,
            level=calculate_level(user.xp),
            words_learned=user.total_words_learned,
            avatar_color=["#8b5cf6", "#ec4899", "#06b6d4", "#10b981"][idx % 4]
        ))
    
    # Определяем, входит ли текущий пользователь в топ
    user_in_top = current_user_rank <= limit
    
    return {
        "period": period,
        "leaderboard": leaderboard,
        "current_user": {
            "rank": current_user_rank,
            "user_id": current_user.id,
            "username": current_user.username,
            "first_name": current_user.first_name,
            "xp": current_user.xp,
            "level": calculate_level(current_user.xp),
            "words_learned": current_user.total_words_learned
        },
        "in_top": user_in_top,
        "total_users": await db.execute(select(func.count(User.id))).scalar()
    }


@router.get("/stats/achievements", response_model=List[AchievementResponse])
async def get_achievements(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить все достижения и прогресс пользователя
    """
    # Получаем все достижения
    achievements_result = await db.execute(select(Achievement))
    all_achievements = achievements_result.scalars().all()
    
    # Получаем ID достижений, которые заработал пользователь
    earned_result = await db.execute(
        select(user_achievements_table.c.achievement_id, user_achievements_table.c.earned_at)
        .where(user_achievements_table.c.user_id == current_user.id)
    )
    earned_dict = {row[0]: row[1] for row in earned_result.fetchall()}
    
    # Рассчитываем прогресс для каждого достижения
    achievements_response = []
    
    for ach in all_achievements:
        progress_current = 0
        progress_target = ach.requirement_value
        
        # Рассчитываем текущий прогресс в зависимости от типа
        if ach.requirement_type == "words":
            progress_current = current_user.total_words_learned
        
        elif ach.requirement_type == "streak":
            progress_current = current_user.streak
        
        elif ach.requirement_type == "lessons":
            progress_current = current_user.total_lessons_completed
        
        elif ach.requirement_type == "level":
            progress_current = current_user.level
        
        elif ach.requirement_type == "friends":
            # Количество друзей
            progress_current = len(current_user.friends)
        
        earned = ach.id in earned_dict
        
        progress_percent = min(100, int((progress_current / progress_target) * 100)) if progress_target > 0 else 0
        
        achievements_response.append(AchievementResponse(
            id=ach.id,
            name=ach.name,
            description=ach.description,
            icon=ach.icon,
            earned=earned,
            earned_at=earned_dict.get(ach.id).isoformat() if earned else None,
            progress=progress_percent if not earned else 100,
            progress_current=progress_current,
            progress_target=progress_target
        ))
    
    return achievements_response


@router.get("/stats/languages-progress", response_model=List[LanguageProgress])
async def get_languages_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Прогресс по каждому языку
    """
    # Получаем все активные языки
    languages_result = await db.execute(
        select(Language).where(Language.is_active == True)
    )
    languages = languages_result.scalars().all()
    
    # Для каждого языка считаем количество выученных слов
    languages_progress = []
    
    for lang in languages:
        # Считаем уникальные слова, которые пользователь правильно ответил хотя бы раз
        words_count_result = await db.execute(
            select(func.count(func.distinct(UserWordProgress.word_id)))
            .join(Word, Word.id == UserWordProgress.word_id)
            .where(
                UserWordProgress.user_id == current_user.id,
                Word.language_id == lang.id,
                UserWordProgress.times_correct > 0
            )
        )
        words_learned = words_count_result.scalar() or 0
        
        # Уровень прогресса (грубая оценка)
        total_words_for_level = 500  # примерное количество слов для уровня B1
        level_progress = min(100, int((words_learned / total_words_for_level) * 100))
        
        # Определяем текущий уровень
        if words_learned < 100:
            current_level = "A1"
        elif words_learned < 300:
            current_level = "A2"
        elif words_learned < 600:
            current_level = "B1"
        elif words_learned < 1000:
            current_level = "B2"
        elif words_learned < 2000:
            current_level = "C1"
        else:
            current_level = "C2"
        
        languages_progress.append(LanguageProgress(
            language_code=lang.code,
            language_name=lang.name,
            flag=lang.flag,
            words_learned=words_learned,
            level_progress=level_progress,
            current_level=current_level
        ))
    
    return languages_progress


@router.get("/stats/weekly-activity")
async def get_weekly_activity(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Активность за последние 7 дней
    """
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=6)
    
    # Получаем статистику по дням
    result = await db.execute(
        select(
            func.date(UserWordProgress.last_practiced).label("day"),
            func.count(UserWordProgress.id).label("words"),
            func.sum(UserWordProgress.times_correct * 10).label("xp")
        )
        .where(UserWordProgress.user_id == current_user.id)
        .where(func.date(UserWordProgress.last_practiced) >= week_ago)
        .where(func.date(UserWordProgress.last_practiced) <= today)
        .group_by(func.date(UserWordProgress.last_practiced))
    )
    
    daily_data = {row.day: {"words": row.words, "xp": row.xp or 0} for row in result.fetchall()}
    
    # Формируем массив за 7 дней
    week_days = []
    day_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    
    for i in range(7):
        current_day = week_ago + timedelta(days=i)
        day_str = current_day.isoformat()
        data = daily_data.get(day_str, {"words": 0, "xp": 0})
        
        week_days.append(WeeklyActivity(
            day=day_names[current_day.weekday()],
            words=data["words"],
            xp=data["xp"]
        ))
    
    return {
        "week_activity": week_days,
        "total_words": sum(d["words"] for d in daily_data.values()),
        "total_xp": sum(d["xp"] for d in daily_data.values())
    }


@router.get("/stats/daily-tasks")
async def get_daily_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Denpend(get_db)
):
    """
    Получить ежедневные задания
    """
    today = datetime.utcnow().date()
    today_start = datetime(today.year, today.month, today.day)
    today_end = today_start + timedelta(days=1)
    
    # Получаем задания пользователя на сегодня
    tasks_result = await db.execute(
        select(UserDailyTask)
        .where(UserDailyTask.user_id == current_user.id)
        .where(UserDailyTask.date >= today_start)
        .where(UserDailyTask.date < today_end)
    )
    user_tasks = tasks_result.scalars().all()
    
    # Если заданий нет — создаём
    if not user_tasks:
        # TODO: создать стандартные ежедневные задания
        pass
    
    return [
        {
            "id": task.id,
            "title": "Выучить 10 слов",
            "description": "Правильно ответь на 10 карточек",
            "progress": task.progress,
            "target": 10,
            "completed": task.completed,
            "claimed": task.claimed,
            "xp_reward": 30,
            "coins_reward": 10
        }
        for task in user_tasks
    ]


@router.post("/stats/daily-tasks/{task_id}/claim")
async def claim_daily_task_reward(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить награду за выполненное задание
    """
    task_result = await db.execute(
        select(UserDailyTask).where(
            UserDailyTask.id == task_id,
            UserDailyTask.user_id == current_user.id
        )
    )
    task = task_result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if not task.completed:
        raise HTTPException(status_code=400, detail="Task not completed yet")
    
    if task.claimed:
        raise HTTPException(status_code=400, detail="Reward already claimed")
    
    # Начисляем награду
    xp_reward = 30  # TODO: брать из конфига задания
    coins_reward = 10
    
    current_user.xp += xp_reward
    current_user.coins += coins_reward
    
    task.claimed = True
    
    await db.commit()
    
    return {
        "message": "Reward claimed!",
        "xp_gained": xp_reward,
        "coins_gained": coins_reward
    }