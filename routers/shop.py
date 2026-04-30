"""
Aevi - Shop Router
Файл: app/routers/shop.py
Магазин, монеты, покупки, скины, бустеры
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field

from app.database.session import get_db
from app.database.models import User, ShopItem, UserPurchase
from app.routers.auth import get_current_user

router = APIRouter()

# Модели ответов/запросов
class ShopItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: str  # theme, hint, bonus, powerup, streak_freeze
    price: int
    icon: str
    is_limited: bool
    expires_at: Optional[str]
    already_owned: bool = False
    data: Optional[dict] = None

class PurchaseRequest(BaseModel):
    item_id: int

class PurchaseResponse(BaseModel):
    success: bool
    item_name: str
    price_paid: int
    coins_remaining: int
    message: str

class UserInventoryResponse(BaseModel):
    themes: List[dict]
    powerups: List[dict]
    active_theme: Optional[str]
    active_boosters: List[dict]

class BoostActivateRequest(BaseModel):
    booster_type: str  # xp_boost, coins_boost, instant_review


# Типы товаров
ITEM_TYPES = {
    "theme": "Тема оформления",
    "hint": "Подсказка (5 шт)",
    "bonus": "Бонусный набор",
    "powerup": "Бустер XP x2",
    "streak_freeze": "Заморозка серии",
    "special": "Особый предмет"
}

# Начальные товары в магазине
DEFAULT_SHOP_ITEMS = [
    # Темы
    {"name": "🌙 Тёмная тема", "description": "Тёмная тема оформления", "type": "theme", "price": 100, "icon": "🌙", "data": {"theme_color": "dark"}},
    {"name": "☀️ Светлая тема", "description": "Светлая тема оформления", "type": "theme", "price": 100, "icon": "☀️", "data": {"theme_color": "light"}},
    {"name": "🎨 Неон-про", "description": "Неоновая тема + анимация", "type": "theme", "price": 250, "icon": "🎨", "data": {"theme_color": "neon_pro", "animation": True}},
    {"name": "🐉 Дракон", "description": "Тема с драконом (редкая)", "type": "theme", "price": 500, "icon": "🐉", "data": {"theme_color": "dragon", "rare": True}},
    
    # Бустеры
    {"name": "⚡ XP Бустер x2 (24ч)", "description": "Удваивает XP на 24 часа", "type": "powerup", "price": 150, "icon": "⚡", "data": {"boost_type": "xp", "multiplier": 2, "duration_hours": 24}},
    {"name": "🪙 Монетный дождь (24ч)", "description": "+50% монет за уроки", "type": "powerup", "price": 120, "icon": "🪙", "data": {"boost_type": "coins", "multiplier": 1.5, "duration_hours": 24}},
    {"name": "🧠 Мгновенное повторение", "description": "Повторить забытые слова", "type": "powerup", "price": 80, "icon": "🧠", "data": {"boost_type": "instant_review", "words_count": 10}},
    
    # Подсказки
    {"name": "💡 Подсказка (5 шт)", "description": "5 подсказок для сложных слов", "type": "hint", "price": 50, "icon": "💡", "data": {"hints_count": 5}},
    {"name": "🔍 Супер-подсказка (3 шт)", "description": "Показывает перевод и пример", "type": "hint", "price": 120, "icon": "🔍", "data": {"hints_count": 3, "super": True}},
    
    # Заморозки серии
    {"name": "❄️ Заморозка серии", "description": "Пропусти день без потери серии", "type": "streak_freeze", "price": 60, "icon": "❄️", "data": {"freeze_days": 1}},
    {"name": "❄️❄️ Заморозка+ (3 дня)", "description": "3 дня без потери серии", "type": "streak_freeze", "price": 150, "icon": "❄️", "data": {"freeze_days": 3}},
    
    # Бонусные наборы
    {"name": "📦 Стартовый набор", "description": "100 монет + 50 XP", "type": "bonus", "price": 0, "icon": "📦", "is_limited": True, "data": {"coins": 100, "xp": 50}},
    {"name": "🎁 Подарочный набор", "description": "300 монет + 3 подсказки", "type": "bonus", "price": 200, "icon": "🎁", "data": {"coins": 300, "hints": 3}},
    {"name": "👑 Премиум набор", "description": "1000 монет + тема 'Дракон'", "type": "bonus", "price": 800, "icon": "👑", "data": {"coins": 1000, "theme": "dragon"}},
]


@router.on_event("startup")
async def init_shop_items(db: AsyncSession):
    """Инициализация товаров в магазине при запуске"""
    # Проверяем, есть ли товары
    result = await db.execute(select(ShopItem).limit(1))
    existing = result.scalar_one_or_none()
    
    if not existing:
        for item_data in DEFAULT_SHOP_ITEMS:
            shop_item = ShopItem(**item_data)
            db.add(shop_item)
        await db.commit()
        print("✅ Shop items initialized")


@router.get("/shop/items", response_model=List[ShopItemResponse])
async def get_shop_items(
    item_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список товаров в магазине
    Можно фильтровать по типу: theme, hint, bonus, powerup, streak_freeze
    """
    query = select(ShopItem).where(ShopItem.is_active == True)
    
    if item_type:
        query = query.where(ShopItem.type == item_type)
    
    # Сортируем: сначала бесплатные и неограниченные
    query = query.order_by(ShopItem.price, ShopItem.is_limited.desc())
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    # Получаем ID товаров, которые уже купил пользователь
    purchases_result = await db.execute(
        select(UserPurchase.item_id).where(UserPurchase.user_id == current_user.id)
    )
    purchased_ids = {row[0] for row in purchases_result.fetchall()}
    
    # Для тем отдельно проверяем владение
    themes_purchased = set()
    for purchase_id in purchased_ids:
        item_result = await db.execute(select(ShopItem).where(ShopItem.id == purchase_id))
        item = item_result.scalar_one_or_none()
        if item and item.type == "theme":
            themes_purchased.add(item.name)
    
    response_items = []
    for item in items:
        already_owned = False
        
        if item.type == "theme":
            # Проверяем, не куплена ли уже тема
            # Сохраняем купленные темы в JSON поле пользователя
            purchased_themes = current_user.settings.get("purchased_themes", [])
            already_owned = item.name in purchased_themes or item.name in themes_purchased
        
        elif item.type == "bonus" and item.price == 0:
            # Стартовый набор — только один раз
            already_owned = current_user.settings.get("starter_pack_claimed", False)
        
        response_items.append(ShopItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            type=item.type,
            price=item.price,
            icon=item.icon,
            is_limited=item.is_limited,
            expires_at=item.expires_at.isoformat() if item.expires_at else None,
            already_owned=already_owned,
            data=item.data
        ))
    
    return response_items


@router.post("/shop/buy", response_model=PurchaseResponse)
async def buy_item(
    request: PurchaseRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Купить предмет в магазине за монеты
    """
    # Получаем товар
    item_result = await db.execute(
        select(ShopItem).where(ShopItem.id == request.item_id)
    )
    item = item_result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Проверяем, достаточно ли монет
    if current_user.coins < item.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough coins. Need {item.price}, you have {current_user.coins}"
        )
    
    # Проверяем, не куплен ли уже (для ограниченных предметов)
    if item.type == "bonus" and item.price == 0:
        if current_user.settings.get("starter_pack_claimed"):
            raise HTTPException(status_code=400, detail="Starter pack already claimed")
    
    if item.type == "theme":
        purchased_themes = current_user.settings.get("purchased_themes", [])
        if item.name in purchased_themes:
            raise HTTPException(status_code=400, detail="Theme already purchased")
    
    # Списываем монеты
    current_user.coins -= item.price
    
    # Создаём запись о покупке
    purchase = UserPurchase(
        user_id=current_user.id,
        item_id=item.id,
        price_paid=item.price
    )
    db.add(purchase)
    
    # Применяем эффект от покупки
    message = ""
    
    if item.type == "theme":
        purchased_themes = current_user.settings.get("purchased_themes", [])
        purchased_themes.append(item.name)
        current_user.settings["purchased_themes"] = purchased_themes
        message = f"Тема '{item.name}' добавлена в твою коллекцию! Изменить тему можно в настройках."
    
    elif item.type == "bonus":
        # Начисляем бонус
        if item.data:
            if "coins" in item.data:
                current_user.coins += item.data["coins"]
            if "xp" in item.data:
                current_user.xp += item.data["xp"]
            if "hints" in item.data:
                current_user.settings["hints"] = current_user.settings.get("hints", 0) + item.data["hints"]
        
        if item.price == 0:
            current_user.settings["starter_pack_claimed"] = True
            message = "Стартовый набор получен! +100 монет, +50 XP"
        else:
            message = f"Бонус активирован! {item.data.get('coins', 0)} монет добавлено."
    
    elif item.type == "hint":
        # Добавляем подсказки в инвентарь
        hints_count = item.data.get("hints_count", 5)
        current_user.settings["hints"] = current_user.settings.get("hints", 0) + hints_count
        message = f"{hints_count} подсказок добавлено в твой инвентарь!"
    
    elif item.type == "powerup":
        # Активируем бустер (сохраняем в active_boosters)
        boosters = current_user.settings.get("active_boosters", [])
        boosters.append({
            "type": item.data.get("boost_type"),
            "multiplier": item.data.get("multiplier", 1),
            "expires_at": (datetime.utcnow() + timedelta(hours=item.data.get("duration_hours", 24))).isoformat(),
            "purchased_at": datetime.utcnow().isoformat()
        })
        current_user.settings["active_boosters"] = boosters
        message = f"Бустер активирован на {item.data.get('duration_hours', 24)} часа!"
    
    elif item.type == "streak_freeze":
        # Добавляем заморозку серии
        freeze_days = item.data.get("freeze_days", 1)
        current_user.settings["streak_freezes"] = current_user.settings.get("streak_freezes", 0) + freeze_days
        message = f"{freeze_days} заморозок серии добавлено. При пропуске дня серия не сбросится!"
    
    await db.commit()
    await db.refresh(current_user)
    
    return PurchaseResponse(
        success=True,
        item_name=item.name,
        price_paid=item.price,
        coins_remaining=current_user.coins,
        message=message or f"Ты купил {item.name}!"
    )


@router.get("/shop/inventory", response_model=UserInventoryResponse)
async def get_inventory(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить инвентарь пользователя:
    - купленные темы
    - активные бустеры
    - подсказки
    """
    purchased_themes = current_user.settings.get("purchased_themes", [])
    active_theme = current_user.theme
    
    # Формируем список тем
    themes = []
    for theme_name in purchased_themes:
        themes.append({
            "name": theme_name,
            "is_active": theme_name.lower() == active_theme or 
                        (theme_name == "Неоновая тема" and active_theme == "neon")
        })
    
    # Активные бустеры
    active_boosters = current_user.settings.get("active_boosters", [])
    now = datetime.utcnow()
    
    # Фильтруем просроченные
    valid_boosters = []
    for booster in active_boosters:
        expires_at = datetime.fromisoformat(booster["expires_at"])
        if expires_at > now:
            valid_boosters.append(booster)
        else:
            # Удаляем просроченные
            pass
    
    # Обновляем список активных бустеров
    if len(valid_boosters) != len(active_boosters):
        current_user.settings["active_boosters"] = valid_boosters
        await db.commit()
    
    # Количество подсказок
    hints_count = current_user.settings.get("hints", 0)
    streak_freezes = current_user.settings.get("streak_freezes", 0)
    
    # Преобразуем бустеры для ответа
    boosters_response = []
    for booster in valid_boosters:
        expires_at = datetime.fromisoformat(booster["expires_at"])
        hours_left = int((expires_at - now).total_seconds() / 3600)
        boosters_response.append({
            "type": booster["type"],
            "multiplier": booster["multiplier"],
            "expires_in_hours": hours_left,
            "expires_at": booster["expires_at"]
        })
    
    return UserInventoryResponse(
        themes=themes,
        powerups=boosters_response,
        active_theme=active_theme,
        active_boosters=boosters_response
    )


@router.post("/shop/activate-booster")
async def activate_booster(
    request: BoostActivateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Активировать бустер из инвентаря
    """
    # Проверяем, есть ли такой бустер в инвентаре
    # (для простоты — активируем первый найденный)
    boosters = current_user.settings.get("active_boosters", [])
    
    for booster in boosters:
        if booster["type"] == request.booster_type:
            # Бустер уже активен
            expires_at = datetime.fromisoformat(booster["expires_at"])
            if expires_at > datetime.utcnow():
                raise HTTPException(status_code=400, detail="Booster already active")
            else:
                # Удаляем просроченный
                boosters.remove(booster)
    
    # TODO: активация нового бустера из купленных предметов
    # Пока заглушка
    return {"message": "Booster activated", "type": request.booster_type}


@router.get("/shop/coins/balance")
async def get_coins_balance(
    current_user: User = Depends(get_current_user)
):
    """Получить баланс монет"""
    return {
        "coins": current_user.coins,
        "earned_today": 0,  # TODO: считать заработанные сегодня
        "spent_today": 0
    }


@router.post("/shop/coins/daily-reward")
async def claim_daily_reward(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ежедневная награда (монеты за вход)
    """
    now = datetime.utcnow()
    today = now.date()
    
    last_claimed = current_user.settings.get("last_daily_reward")
    
    if last_claimed:
        last_date = datetime.fromisoformat(last_claimed).date()
        if last_date == today:
            raise HTTPException(status_code=400, detail="Daily reward already claimed today")
        
        # Проверяем, не пропустил ли пользователь день
        if (today - last_date).days > 1:
            # Сбрасываем счётчик последовательных дней
            current_user.settings["daily_reward_streak"] = 0
    
    # Получаем текущую серию
    streak = current_user.settings.get("daily_reward_streak", 0)
    
    # Рассчитываем награду
    base_reward = 20
    streak_bonus = min(10, streak) * 2  # до +20 монет за серию
    reward = base_reward + streak_bonus
    
    # Начисляем
    current_user.coins += reward
    current_user.settings["daily_reward_streak"] = streak + 1
    current_user.settings["last_daily_reward"] = now.isoformat()
    
    await db.commit()
    
    return {
        "claimed": True,
        "reward": reward,
        "streak": streak + 1,
        "new_balance": current_user.coins
    }