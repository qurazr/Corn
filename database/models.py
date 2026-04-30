"""
Aevi - Database Models
Файл: app/database/models.py
Все модели данных для изучения языков
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, JSON, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

Base = declarative_base()

# Ассоциативная таблица "друзья" (многие ко многим)
friends_table = Table(
    "friends",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("friend_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("status", String, default="pending")  # pending, accepted, blocked
)

# Ассоциативная таблица "достижения пользователя"
user_achievements_table = Table(
    "user_achievements",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("achievement_id", Integer, ForeignKey("achievements.id"), primary_key=True),
    Column("earned_at", DateTime, default=datetime.utcnow)
)


class User(Base):
    """Пользователь Telegram"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(64), nullable=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=True)
    
    # Статистика
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    coins = Column(Integer, default=100)
    streak = Column(Integer, default=0)  # дней подряд
    total_words_learned = Column(Integer, default=0)
    total_lessons_completed = Column(Integer, default=0)
    total_time_spent = Column(Integer, default=0)  # минут
    
    # Настройки
    current_language = Column(String(10), default="en")  # en, es, de, fr, th, zh, ja, ko
    daily_goal = Column(Integer, default=20)  # слов в день
    theme = Column(String(20), default="neon")  # neon, dark, light
    notifications_enabled = Column(Boolean, default=True)
    
    # Даты
    registered_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    last_streak_update = Column(DateTime, nullable=True)
    
    # Relationships
    progress = relationship("UserWordProgress", back_populates="user", cascade="all, delete-orphan")
    lessons = relationship("UserLesson", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("Achievement", secondary=user_achievements_table, back_populates="users")
    friends = relationship(
        "User",
        secondary=friends_table,
        primaryjoin=id == friends_table.c.user_id,
        secondaryjoin=id == friends_table.c.friend_id,
        backref="friend_of"
    )
    purchases = relationship("UserPurchase", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "tg_id": self.tg_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "xp": self.xp,
            "level": self.level,
            "coins": self.coins,
            "streak": self.streak,
            "total_words_learned": self.total_words_learned,
            "current_language": self.current_language,
            "daily_goal": self.daily_goal,
            "theme": self.theme
        }


class Language(Base):
    """Доступные языки"""
    __tablename__ = "languages"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)  # en, es, de, fr, th, zh, ja, ko
    name = Column(String(50), nullable=False)  # English, Español, etc.
    flag = Column(String(10))  # 🇬🇧, 🇪🇸
    is_active = Column(Boolean, default=True)
    
    # Relationships
    words = relationship("Word", back_populates="language", cascade="all, delete-orphan")
    lessons = relationship("Lesson", back_populates="language", cascade="all, delete-orphan")


class Word(Base):
    """Слово для изучения"""
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    word = Column(String(200), nullable=False, index=True)
    translation = Column(String(200), nullable=False)
    transcription = Column(String(100), nullable=True)
    example = Column(Text, nullable=True)  # пример использования
    example_translation = Column(Text, nullable=True)
    
    # Категории
    level = Column(String(5), default="A1")  # A1, A2, B1, B2, C1
    topic = Column(String(50), default="general")  # family, travel, business, etc.
    part_of_speech = Column(String(20))  # noun, verb, adjective, etc.
    
    # Медиа
    image_url = Column(String(500), nullable=True)
    audio_url = Column(String(500), nullable=True)
    
    # Сложность (1-5)
    difficulty = Column(Integer, default=1)
    
    # Relationships
    language = relationship("Language", back_populates="words")
    user_progress = relationship("UserWordProgress", back_populates="word", cascade="all, delete-orphan")


class UserWordProgress(Base):
    """Прогресс пользователя по словам (Spaced Repetition SM-2)"""
    __tablename__ = "user_word_progress"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    
    # SM-2 алгоритм
    repetitions = Column(Integer, default=0)  # количество повторений
    interval = Column(Integer, default=0)  # интервал в днях
    efactor = Column(Float, default=2.5)  # фактор лёгкости
    next_review = Column(DateTime, default=datetime.utcnow)  # когда повторять
    
    # Статистика по слову
    times_correct = Column(Integer, default=0)
    times_incorrect = Column(Integer, default=0)
    last_practiced = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    word = relationship("Word", back_populates="user_progress")


class Lesson(Base):
    """Урок по определённой теме"""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    topic = Column(String(50), nullable=False)
    level = Column(String(5), nullable=False)
    
    # Количественные показатели
    words_count = Column(Integer, default=10)
    order_index = Column(Integer, default=0)  # порядок прохождения
    xp_reward = Column(Integer, default=50)
    coins_reward = Column(Integer, default=10)
    
    # Relationships
    language = relationship("Language", back_populates="lessons")
    user_lessons = relationship("UserLesson", back_populates="lesson", cascade="all, delete-orphan")


class UserLesson(Base):
    """Прогресс пользователя по урокам"""
    __tablename__ = "user_lessons"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    
    completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)  # 0-100%
    completed_at = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="lessons")
    lesson = relationship("Lesson", back_populates="user_lessons")


class Achievement(Base):
    """Достижения для геймификации"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), nullable=False)  # 🏆, 🔥, 💪
    xp_reward = Column(Integer, default=100)
    coins_reward = Column(Integer, default=50)
    
    # Условия получения
    requirement_type = Column(String(50))  # words, streak, lessons, level, friends
    requirement_value = Column(Integer)  # сколько нужно
    
    # Relationships
    users = relationship("User", secondary=user_achievements_table, back_populates="achievements")


class ShopItem(Base):
    """Предметы в магазине"""
    __tablename__ = "shop_items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)  # theme, hint, bonus, powerup
    price = Column(Integer, nullable=False)
    icon = Column(String(50), nullable=False)
    
    # Дополнительные данные (JSON)
    data = Column(JSON, default=dict)  # {"theme_color": "#ff00ff", "boost_percent": 20}
    
    is_active = Column(Boolean, default=True)
    is_limited = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)


class UserPurchase(Base):
    """Покупки пользователя"""
    __tablename__ = "user_purchases"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("shop_items.id"), nullable=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)
    price_paid = Column(Integer, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="purchases")
    item = relationship("ShopItem")


class DailyTask(Base):
    """Ежедневные задания"""
    __tablename__ = "daily_tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    task_type = Column(String(50))  # learn_words, complete_lesson, streak, share
    target = Column(Integer, nullable=False)  # сколько сделать
    xp_reward = Column(Integer, default=30)
    coins_reward = Column(Integer, default=10)
    
    is_active = Column(Boolean, default=True)


class UserDailyTask(Base):
    """Прогресс пользователя по ежедневным заданиям"""
    __tablename__ = "user_daily_tasks"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("daily_tasks.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    claimed = Column(Boolean, default=False)


class LeaderboardCache(Base):
    """Кэш таблицы лидеров (обновляется раз в час)"""
    __tablename__ = "leaderboard_cache"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    rank = Column(Integer)
    score = Column(Integer)  # XP или количество слов
    period = Column(String(20), default="all_time")  # daily, weekly, monthly, all_time
    updated_at = Column(DateTime, default=datetime.utcnow)