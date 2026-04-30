"""
Aevi - Configuration
Файл: app/config.py
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Все настройки приложения в одном месте"""
    
    # Telegram
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    BOT_USERNAME: str = os.getenv("BOT_USERNAME", "AeviLangBot")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aevi.db")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    
    # Redis (для кэша и leaderboard)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AI / LLM
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
    
    # TTS (озвучка)
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS (для фронтенда)
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173,https://aevi.app").split(",")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-me")
    JWT_EXPIRE_HOURS: int = int(os.getenv("JWT_EXPIRE_HOURS", "720"))  # 30 дней
    
    # Admin
    ADMIN_IDS: List[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
    
    # Features
    ENABLE_VOICE_TRAINING: bool = True
    ENABLE_AI_CHAT: bool = True
    DAILY_GOAL_XP: int = 100
    STREAK_BONUS_XP: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Проверка обязательных переменных
if not settings.BOT_TOKEN and not settings.DEBUG:
    raise ValueError("BOT_TOKEN is required in production mode!")