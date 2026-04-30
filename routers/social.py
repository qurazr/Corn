"""
Aevi - Social Router
Файл: app/routers/social.py
Друзья, челленджи, таблица лидеров среди друзей, общий чат
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc, update, delete
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field
import random

from app.database.session import get_db
from app.database.models import User, friends_table
from app.routers.auth import get_current_user
from app.routers.learning import calculate_level

router = APIRouter()

# Модели запросов/ответов
class FriendRequest(BaseModel):
    friend_username: str

class FriendResponse(BaseModel):
    id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    level: int
    streak: int
    xp: int
    status: str  # pending, accepted, blocked
    common_friends: int = 0
    avatar_color: str = "#8b5cf6"

class ChallengeResponse(BaseModel):
    id: int
    name: str
    description: str
    type: str  # words, xp, streak, lessons
    goal: int
    prize_xp: int
    prize_coins: int
    participants: List[dict]
    my_progress: int
    ends_at: str
    is_active: bool

class LeaderboardFriendResponse(BaseModel):
    rank: int
    user_id: int
    username: Optional[str]
    first_name: str
    xp: int
    level: int
    is_friend: bool


@router.get("/social/friends", response_model=List[FriendResponse])
async def get_friends(
    status: Optional[str] = "accepted",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список друзей
    status: pending, accepted, blocked
    """
    # Получаем друзей пользователя
    if status == "accepted":
        query = select(User).join(
            friends_table,
            or_(
                and_(
                    friends_table.c.user_id == current_user.id,
                    friends_table.c.friend_id == User.id,
                    friends_table.c.status == "accepted"
                ),
                and_(
                    friends_table.c.friend_id == current_user.id,
                    friends_table.c.user_id == User.id,
                    friends_table.c.status == "accepted"
                )
            )
        )
    elif status == "pending":
        # Заявки, которые отправили друзья текущему пользователю
        query = select(User).join(
            friends_table,
            and_(
                friends_table.c.user_id == User.id,
                friends_table.c.friend_id == current_user.id,
                friends_table.c.status == "pending"
            )
        )
    else:
        query = select(User).join(
            friends_table,
            or_(
                and_(
                    friends_table.c.user_id == current_user.id,
                    friends_table.c.friend_id == User.id,
                    friends_table.c.status == status
                ),
                and_(
                    friends_table.c.friend_id == current_user.id,
                    friends_table.c.user_id == User.id,
                    friends_table.c.status == status
                )
            )
        )
    
    result = await db.execute(query)
    friends = result.scalars().all()
    
    friends_response = []
    for friend in friends:
        # Считаем общих друзей (для статистики)
        common_query = select(func.count()).select_from(friends_table).where(
            and_(
                friends_table.c.user_id.in_([current_user.id, friend.id]),
                friends_table.c.friend_id.in_([current_user.id, friend.id]),
                friends_table.c.status == "accepted"
            )
        )
        common_result = await db.execute(common_query)
        common_friends = common_result.scalar() or 0
        
        friends_response.append(FriendResponse(
            id=friend.id,
            username=friend.username,
            first_name=friend.first_name,
            last_name=friend.last_name,
            level=calculate_level(friend.xp),
            streak=friend.streak,
            xp=friend.xp,
            status=status,
            common_friends=common_friends // 2,  # делим на 2, так как связь двусторонняя
            avatar_color=f"#{hash(friend.username or friend.first_name) % 0xFFFFFF:06x}"
        ))
    
    return friends_response


@router.post("/social/friends/add")
async def add_friend(
    request: FriendRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Отправить заявку в друзья по username
    """
    # Ищем пользователя по username
    result = await db.execute(
        select(User).where(User.username == request.friend_username)
    )
    friend = result.scalar_one_or_none()
    
    if not friend:
        raise HTTPException(status_code=404, detail="User not found")
    
    if friend.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot add yourself as friend")
    
    # Проверяем, не отправлена ли уже заявка
    existing = await db.execute(
        select(friends_table).where(
            or_(
                and_(
                    friends_table.c.user_id == current_user.id,
                    friends_table.c.friend_id == friend.id
                ),
                and_(
                    friends_table.c.user_id == friend.id,
                    friends_table.c.friend_id == current_user.id
                )
            )
        )
    )
    existing_rel = existing.scalar_one_or_none()
    
    if existing_rel:
        if existing_rel.status == "accepted":
            raise HTTPException(status_code=400, detail="Already friends")
        elif existing_rel.status == "pending":
            raise HTTPException(status_code=400, detail="Friend request already sent")
    
    # Создаём заявку
    stmt = friends_table.insert().values(
        user_id=current_user.id,
        friend_id=friend.id,
        status="pending",
        created_at=datetime.utcnow()
    )
    await db.execute(stmt)
    await db.commit()
    
    return {"message": f"Friend request sent to {friend.first_name}"}


@router.post("/social/friends/{friend_id}/accept")
async def accept_friend(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Принять заявку в друзья
    """
    # Находим заявку
    stmt = select(friends_table).where(
        and_(
            friends_table.c.user_id == friend_id,
            friends_table.c.friend_id == current_user.id,
            friends_table.c.status == "pending"
        )
    )
    result = await db.execute(stmt)
    friend_rel = result.scalar_one_or_none()
    
    if not friend_rel:
        raise HTTPException(status_code=404, detail="Friend request not found")
    
    # Обновляем статус
    update_stmt = update(friends_table).where(
        and_(
            friends_table.c.user_id == friend_id,
            friends_table.c.friend_id == current_user.id
        )
    ).values(status="accepted")
    
    await db.execute(update_stmt)
    await db.commit()
    
    return {"message": "Friend request accepted"}


@router.delete("/social/friends/{friend_id}/remove")
async def remove_friend(
    friend_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить из друзей или отклонить заявку
    """
    delete_stmt = delete(friends_table).where(
        or_(
            and_(
                friends_table.c.user_id == current_user.id,
                friends_table.c.friend_id == friend_id
            ),
            and_(
                friends_table.c.user_id == friend_id,
                friends_table.c.friend_id == current_user.id
            )
        )
    )
    
    result = await db.execute(delete_stmt)
    await db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Friendship not found")
    
    return {"message": "Friend removed"}


@router.get("/social/leaderboard/friends")
async def get_friends_leaderboard(
    period: str = "weekly",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Таблица лидеров среди друзей
    period: daily, weekly, monthly, all_time
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
    
    # Получаем ID друзей пользователя
    friends_query = select(friends_table.c.user_id, friends_table.c.friend_id).where(
        or_(
            friends_table.c.user_id == current_user.id,
            friends_table.c.friend_id == current_user.id
        ),
        friends_table.c.status == "accepted"
    )
    friends_result = await db.execute(friends_query)
    friend_ids = set()
    for row in friends_result.fetchall():
        if row.user_id == current_user.id:
            friend_ids.add(row.friend_id)
        else:
            friend_ids.add(row.user_id)
    
    # Добавляем самого пользователя
    friend_ids.add(current_user.id)
    
    # Получаем лидерборд среди друзей
    if start_date:
        # Считаем активность за период
        # TODO: агрегировать XP из UserWordProgress за период
        query = select(User).where(User.id.in_(friend_ids)).order_by(desc(User.xp))
    else:
        query = select(User).where(User.id.in_(friend_ids)).order_by(desc(User.xp))
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    leaderboard = []
    for idx, user in enumerate(users, 1):
        leaderboard.append(LeaderboardFriendResponse(
            rank=idx,
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            xp=user.xp,
            level=calculate_level(user.xp),
            is_friend=user.id != current_user.id
        ))
    
    return {
        "period": period,
        "leaderboard": leaderboard,
        "my_rank": next((i+1 for i, u in enumerate(users) if u.id == current_user.id), None)
    }


# Простые челленджи (без отдельной модели в БД для простоты)
CHALLENGES = [
    {
        "id": 1,
        "name": "🏆 Битва слов",
        "description": "Кто выучит больше новых слов за 7 дней",
        "type": "words",
        "goal": 50,
        "prize_xp": 500,
        "prize_coins": 200
    },
    {
        "id": 2,
        "name": "⚡ Гонка XP",
        "description": "Набери максимальное количество опыта",
        "type": "xp",
        "goal": 1000,
        "prize_xp": 300,
        "prize_coins": 150
    },
    {
        "id": 3,
        "name": "🔥 Неделя силы",
        "description": "Не пропускай занятия 7 дней подряд",
        "type": "streak",
        "goal": 7,
        "prize_xp": 400,
        "prize_coins": 100
    }
]


@router.get("/social/challenges", response_model=List[ChallengeResponse])
async def get_active_challenges(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить активные челленджи
    """
    # В реальном приложении челленджи хранятся в БД
    # Здесь используем заглушку
    
    challenges_response = []
    for challenge in CHALLENGES:
        # Получаем прогресс пользователя (заглушка)
        my_progress = random.randint(0, challenge["goal"])
        
        # Участники (заглушка)
        participants = [
            {"user_id": 1, "name": "Анна", "progress": 45},
            {"user_id": 2, "name": "Максим", "progress": 38},
            {"user_id": current_user.id, "name": current_user.first_name, "progress": my_progress, "is_me": True}
        ]
        participants.sort(key=lambda x: x["progress"], reverse=True)
        
        challenges_response.append(ChallengeResponse(
            id=challenge["id"],
            name=challenge["name"],
            description=challenge["description"],
            type=challenge["type"],
            goal=challenge["goal"],
            prize_xp=challenge["prize_xp"],
            prize_coins=challenge["prize_coins"],
            participants=participants[:5],
            my_progress=my_progress,
            ends_at=(datetime.utcnow() + timedelta(days=7)).isoformat(),
            is_active=True
        ))
    
    return challenges_response


@router.post("/social/challenges/{challenge_id}/join")
async def join_challenge(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Присоединиться к челленджу
    """
    # Проверяем существование челленджа
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    # Сохраняем участие в БД (в реальном приложении)
    # current_user.settings["joined_challenges"] = ...
    
    return {"message": f"Joined challenge: {challenge['name']}"}


@router.get("/social/search")
async def search_users(
    query: str,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Поиск пользователей по имени или username
    """
    search_pattern = f"%{query}%"
    
    result = await db.execute(
        select(User)
        .where(
            or_(
                User.username.ilike(search_pattern),
                User.first_name.ilike(search_pattern),
                User.last_name.ilike(search_pattern)
            ),
            User.id != current_user.id
        )
        .limit(limit)
    )
    users = result.scalars().all()
    
    # Получаем ID друзей
    friends_result = await db.execute(
        select(friends_table.c.user_id, friends_table.c.friend_id).where(
            or_(
                friends_table.c.user_id == current_user.id,
                friends_table.c.friend_id == current_user.id
            ),
            friends_table.c.status == "accepted"
        )
    )
    friend_ids = set()
    for row in friends_result.fetchall():
        if row.user_id == current_user.id:
            friend_ids.add(row.friend_id)
        else:
            friend_ids.add(row.user_id)
    
    return [
        {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "level": calculate_level(user.xp),
            "streak": user.streak,
            "is_friend": user.id in friend_ids
        }
        for user in users
    ]


@router.get("/social/stats")
async def get_social_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить социальную статистику
    """
    # Количество друзей
    friends_result = await db.execute(
        select(friends_table).where(
            or_(
                friends_table.c.user_id == current_user.id,
                friends_table.c.friend_id == current_user.id
            ),
            friends_table.c.status == "accepted"
        )
    )
    friends_count = friends_result.rowcount
    
    # Количество входящих заявок
    incoming_result = await db.execute(
        select(friends_table).where(
            friends_table.c.friend_id == current_user.id,
            friends_table.c.status == "pending"
        )
    )
    incoming_requests = incoming_result.rowcount
    
    # Количество активных челленджей
    active_challenges = len(CHALLENGES)
    
    return {
        "friends_count": friends_count,
        "incoming_requests": incoming_requests,
        "active_challenges": active_challenges,
        "global_rank": None  # TODO: рассчитать глобальный ранг
    }