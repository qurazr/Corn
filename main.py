"""
Aevi - Language Learning Mini App
Backend entry point: main.py
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

from app.config import settings
from app.database.session import engine, init_db
from app.routers import auth, learning, stats, shop, social, ai, admin
from app.middlewares import AuthMiddleware, LoggingMiddleware

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("aevi")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    logger.info("🚀 Aevi запускается...")
    
    # Инициализация базы данных
    await init_db()
    logger.info("✅ База данных подключена")
    
    # Здесь можно загрузить слова в БД при первом запуске
    # await seed_database()
    
    yield
    
    # Закрытие соединений при выключении
    await engine.dispose()
    logger.info("👋 Aevi остановлен")

# Создание приложения
app = FastAPI(
    title="Aevi API",
    description="Language Learning Mini App для Telegram",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None
)

# CORS настройки (для разработки и продакшена)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Кастомные мидлвари
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# Подключение роутеров
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])
app.include_router(shop.router, prefix="/api/shop", tags=["Shop"])
app.include_router(social.router, prefix="/api/social", tags=["Social"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI Assistant"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

# Health check для мониторинга
@app.get("/health", tags=["System"])
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "aevi", "version": "1.0.0"}
    )

# Корневой эндпоинт
@app.get("/", tags=["System"])
async def root():
    return {
        "name": "Aevi Language Learning",
        "version": "1.0.0",
        "status": "active",
        "documentation": "/api/docs"
    }

# Обработчик 404
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": str(request.url)}
    )

# Запуск (для локальной разработки)
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )