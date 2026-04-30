"""
Aevi - Database Session Management
Файл: app/database/session.py
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

from app.config import settings
from app.database.models import Base

# Создание движка БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # логирование SQL в DEBUG режиме
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=20,
    pool_pre_ping=True,  # проверка соединения перед использованием
)

# Фабрика сессий
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии БД"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Инициализация БД: создание всех таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Проверка: если языков нет — добавить базовые
    await seed_languages()

async def seed_languages():
    """Добавляем 8 языков при первом запуске"""
    from sqlalchemy import select
    
    async with async_session_maker() as session:
        result = await session.execute(select(Base.metadata.tables["languages"]))
        # Проверяем, пустая ли таблица
        count = result.rowcount
        
        if count == 0:
            languages = [
                {"code": "en", "name": "English", "flag": "🇬🇧"},
                {"code": "es", "name": "Español", "flag": "🇪🇸"},
                {"code": "de", "name": "Deutsch", "flag": "🇩🇪"},
                {"code": "fr", "name": "Français", "flag": "🇫🇷"},
                {"code": "th", "name": "ไทย", "flag": "🇹🇭"},
                {"code": "zh", "name": "中文", "flag": "🇨🇳"},
                {"code": "ja", "name": "日本語", "flag": "🇯🇵"},
                {"code": "ko", "name": "한국어", "flag": "🇰🇷"},
            ]
            
            from app.database.models import Language
            for lang in languages:
                session.add(Language(**lang))
            
            await session.commit()
            print("✅ 8 языков добавлены в БД")