"""
Aevi - Learning Router
Файл: app/routers/learning.py
Уроки, слова, упражнения, Spaced Repetition
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import random

from app.database.session import get_db
from app.database.models import User, Word, Language, UserWordProgress, Lesson, UserLesson
from app.routers.auth import get_current_user

router = APIRouter()

# Модели запросов/ответов
class WordCardResponse(BaseModel):
    id: int
    word: str
    translation: str
    transcription: Optional[str]
    example: Optional[str]
    example_translation: Optional[str]
    image_url: Optional[str]
    part_of_speech: Optional[str]

class CheckAnswerRequest(BaseModel):
    word_id: int
    user_answer: str
    exercise_type: str = "translation"  # translation, writing, listening

class CheckAnswerResponse(BaseModel):
    correct: bool
    correct_answer: str
    xp_gained: int
    coins_gained: int
    next_review: Optional[str]

class LessonResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    topic: str
    level: str
    words_count: int
    xp_reward: int
    completed: bool = False
    progress: int = 0  # % выполнения

class StartLessonResponse(BaseModel):
    lesson_id: int
    words: List[WordCardResponse]
    total_words: int


# Константы для XP
XP_PER_CORRECT_WORD = 10
XP_PER_CORRECT_WORD_STREAK_BONUS = 5
COINS_PER_CORRECT_WORD = 2
STREAK_MULTIPLIER_DAYS = 7  # после 7 дней множитель x2


def calculate_xp_reward(streak_days: int, is_correct: bool) -> tuple[int, int]:
    """Рассчитывает награду за правильный ответ"""
    if not is_correct:
        return 0, 0
    
    xp = XP_PER_CORRECT_WORD
    coins = COINS_PER_CORRECT_WORD
    
    # Бонус за streak
    if streak_days >= STREAK_MULTIPLIER_DAYS:
        xp += XP_PER_CORRECT_WORD_STREAK_BONUS
    
    return xp, coins


def update_sm2(quality: int, repetitions: int, interval: int, efactor: float) -> tuple[int, float, int]:
    """
    Алгоритм SM-2 (SuperMemo 2)
    quality: 0-5 (0=полный провал, 5=идеально)
    возвращает: (новый_интервал, новый_efactor, новые_повторения)
    """
    if quality < 2:
        # Неправильно — сбрасываем
        return 0, efactor, 0
    
    if repetitions == 0:
        interval = 1
    elif repetitions == 1:
        interval = 6
    else:
        interval = int(interval * efactor)
    
    # Обновляем EF (E-Factor)
    if quality >= 3:
        efactor = efactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    
    # Ограничения EF
    if efactor < 1.3:
        efactor = 1.3
    
    return interval, efactor, repetitions + 1


@router.get("/learning/words/due")
async def get_words_due_for_review(
    limit: int = 20,
    language_code: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить слова, которые нужно повторить (SM-2)
    Возвращает слова, у которых next_review <= сейчас
    """
    lang_code = language_code or current_user.current_language
    
    # Получаем язык
    lang_result = await db.execute(
        select(Language).where(Language.code == lang_code)
    )
    language = lang_result.scalar_one_or_none()
    
    if not language:
        raise HTTPException(status_code=404, detail=f"Language {lang_code} not found")
    
    # Получаем слова пользователя, которые нужно повторить
    query = (
        select(Word)
        .join(UserWordProgress, and_(
            UserWordProgress.word_id == Word.id,
            UserWordProgress.user_id == current_user.id
        ))
        .where(Word.language_id == language.id)
        .where(UserWordProgress.next_review <= datetime.utcnow())
        .order_by(UserWordProgress.next_review)
        .limit(limit)
    )
    
    result = await db.execute(query)
    words = result.scalars().all()
    
    # Если новых слов мало — добавляем новые слова (которые ещё не учил)
    if len(words) < limit:
        # Получаем ID слов, которые пользователь уже видел
        seen_ids_query = select(UserWordProgress.word_id).where(
            UserWordProgress.user_id == current_user.id
        )
        seen_result = await db.execute(seen_ids_query)
        seen_ids = [row[0] for row in seen_result.fetchall()]
        
        # Добавляем новые слова
        new_words_query = (
            select(Word)
            .where(Word.language_id == language.id)
            .where(~Word.id.in_(seen_ids) if seen_ids else True)
            .limit(limit - len(words))
        )
        new_result = await db.execute(new_words_query)
        new_words = new_result.scalars().all()
        words.extend(new_words)
    
    # Преобразуем в ответ
    return [
        WordCardResponse(
            id=w.id,
            word=w.word,
            translation=w.translation,
            transcription=w.transcription,
            example=w.example,
            example_translation=w.example_translation,
            image_url=w.image_url,
            part_of_speech=w.part_of_speech
        )
        for w in words
    ]


@router.post("/learning/check-answer", response_model=CheckAnswerResponse)
async def check_answer(
    request: CheckAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Проверить ответ пользователя и обновить прогресс"""
    
    # Получаем слово
    word_result = await db.execute(
        select(Word).where(Word.id == request.word_id)
    )
    word = word_result.scalar_one_or_none()
    
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Проверяем ответ (в зависимости от типа упражнения)
    is_correct = False
    
    if request.exercise_type == "translation":
        # Сравниваем с переводом (регистронезависимо, убираем лишние пробелы)
        user_clean = request.user_answer.strip().lower()
        correct_clean = word.translation.strip().lower()
        is_correct = user_clean == correct_clean
    
    elif request.exercise_type == "writing":
        # Для написания слова — сравниваем с оригинальным словом
        user_clean = request.user_answer.strip().lower()
        correct_clean = word.word.strip().lower()
        is_correct = user_clean == correct_clean
    
    elif request.exercise_type == "listening":
        # Для аудирования — сравниваем с переводом
        user_clean = request.user_answer.strip().lower()
        correct_clean = word.translation.strip().lower()
        is_correct = user_clean == correct_clean
    
    # Получаем или создаём прогресс по слову
    progress_result = await db.execute(
        select(UserWordProgress).where(
            UserWordProgress.user_id == current_user.id,
            UserWordProgress.word_id == word.id
        )
    )
    progress = progress_result.scalar_one_or_none()
    
    if not progress:
        progress = UserWordProgress(
            user_id=current_user.id,
            word_id=word.id,
            next_review=datetime.utcnow()
        )
        db.add(progress)
    
    # Качество ответа для SM-2 (0-5)
    quality = 5 if is_correct else 1
    
    # Обновляем SM-2
    new_interval, new_efactor, new_repetitions = update_sm2(
        quality=quality,
        repetitions=progress.repetitions,
        interval=progress.interval,
        efactor=progress.efactor
    )
    
    progress.interval = new_interval
    progress.efactor = new_efactor
    progress.repetitions = new_repetitions
    
    # Вычисляем следующий пересмотр
    if new_interval > 0:
        progress.next_review = datetime.utcnow() + timedelta(days=new_interval)
    else:
        progress.next_review = datetime.utcnow() + timedelta(hours=1)  # повторить через час
    
    # Обновляем статистику
    if is_correct:
        progress.times_correct += 1
        
        # Награда
        xp_gain, coins_gain = calculate_xp_reward(current_user.streak, is_correct)
        
        # Проверяем, не впервые ли слово выучено
        if progress.times_correct == 1 and progress.times_incorrect == 0:
            current_user.total_words_learned += 1
        
        current_user.xp += xp_gain
        current_user.coins += coins_gain
        
        # Обновляем уровень (если нужно)
        new_level = calculate_level(current_user.xp)
        if new_level > current_user.level:
            current_user.level = new_level
        
    else:
        progress.times_incorrect += 1
        xp_gain, coins_gain = 0, 0
    
    progress.last_practiced = datetime.utcnow()
    
    await db.commit()
    
    return CheckAnswerResponse(
        correct=is_correct,
        correct_answer=word.translation,
        xp_gained=xp_gain,
        coins_gained=coins_gain,
        next_review=progress.next_review.isoformat() if progress.next_review else None
    )


@router.get("/learning/lessons", response_model=List[LessonResponse])
async def get_lessons(
    language_code: Optional[str] = None,
    level: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить список уроков для языка"""
    lang_code = language_code or current_user.current_language
    
    # Получаем язык
    lang_result = await db.execute(
        select(Language).where(Language.code == lang_code)
    )
    language = lang_result.scalar_one_or_none()
    
    if not language:
        raise HTTPException(status_code=404, detail=f"Language {lang_code} not found")
    
    # Получаем уроки
    query = select(Lesson).where(Lesson.language_id == language.id)
    
    if level:
        query = query.where(Lesson.level == level)
    
    query = query.order_by(Lesson.order_index)
    
    result = await db.execute(query)
    lessons = result.scalars().all()
    
    # Получаем прогресс пользователя по урокам
    lesson_ids = [l.id for l in lessons]
    progress_result = await db.execute(
        select(UserLesson).where(
            UserLesson.user_id == current_user.id,
            UserLesson.lesson_id.in_(lesson_ids)
        )
    )
    progresses = {p.lesson_id: p for p in progress_result.scalars().all()}
    
    # Считаем прогресс по каждому уроку (сколько слов выучено)
    # TODO: реализовать подсчёт % выполнения урока
    
    return [
        LessonResponse(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            topic=lesson.topic,
            level=lesson.level,
            words_count=lesson.words_count,
            xp_reward=lesson.xp_reward,
            completed=lesson.id in progresses and progresses[lesson.id].completed,
            progress=0  # заглушка
        )
        for lesson in lessons
    ]


@router.get("/learning/lessons/{lesson_id}", response_model=StartLessonResponse)
async def start_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Начать урок — получить все слова урока"""
    
    # Получаем урок
    lesson_result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = lesson_result.scalar_one_or_none()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Получаем слова для этого урока (по теме и уровню)
    words_result = await db.execute(
        select(Word)
        .where(Word.language_id == lesson.language_id)
        .where(Word.topic == lesson.topic)
        .where(Word.level == lesson.level)
        .limit(lesson.words_count)
    )
    words = words_result.scalars().all()
    
    # Или если нет слов по теме — берём любые
    if not words:
        words_result = await db.execute(
            select(Word)
            .where(Word.language_id == lesson.language_id)
            .where(Word.level == lesson.level)
            .limit(lesson.words_count)
        )
        words = words_result.scalars().all()
    
    # Создаём запись о начале урока (если нет)
    user_lesson_result = await db.execute(
        select(UserLesson).where(
            UserLesson.user_id == current_user.id,
            UserLesson.lesson_id == lesson_id
        )
    )
    user_lesson = user_lesson_result.scalar_one_or_none()
    
    if not user_lesson:
        user_lesson = UserLesson(
            user_id=current_user.id,
            lesson_id=lesson_id,
            attempts=1
        )
        db.add(user_lesson)
        await db.commit()
    
    return StartLessonResponse(
        lesson_id=lesson_id,
        words=[
            WordCardResponse(
                id=w.id,
                word=w.word,
                translation=w.translation,
                transcription=w.transcription,
                example=w.example,
                example_translation=w.example_translation,
                image_url=w.image_url,
                part_of_speech=w.part_of_speech
            )
            for w in words
        ],
        total_words=len(words)
    )


@router.post("/learning/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    score: int,  # 0-100
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Завершить урок с получением награды"""
    
    # Получаем урок
    lesson_result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    lesson = lesson_result.scalar_one_or_none()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Получаем прогресс пользователя
    user_lesson_result = await db.execute(
        select(UserLesson).where(
            UserLesson.user_id == current_user.id,
            UserLesson.lesson_id == lesson_id
        )
    )
    user_lesson = user_lesson_result.scalar_one_or_none()
    
    if not user_lesson:
        user_lesson = UserLesson(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        db.add(user_lesson)
    
    # Если урок уже завершён — не даём награду повторно
    if user_lesson.completed:
        return {"message": "Lesson already completed", "reward_claimed": False}
    
    # Рассчитываем награду
    xp_reward = int(lesson.xp_reward * (score / 100))
    coins_reward = lesson.coins_reward if score >= 70 else 0
    
    # Начисляем
    current_user.xp += xp_reward
    current_user.coins += coins_reward
    current_user.total_lessons_completed += 1
    
    # Обновляем уровень
    new_level = calculate_level(current_user.xp)
    if new_level > current_user.level:
        current_user.level = new_level
    
    # Завершаем урок
    user_lesson.completed = True
    user_lesson.completed_at = datetime.utcnow()
    user_lesson.score = score
    
    await db.commit()
    
    return {
        "message": "Lesson completed!",
        "reward_claimed": True,
        "xp_gained": xp_reward,
        "coins_gained": coins_reward,
        "total_score": score
    }


def calculate_level(xp: int) -> int:
    """Расчёт уровня по XP"""
    level = 1
    xp_needed = 100
    
    while xp >= xp_needed:
        xp -= xp_needed
        level += 1
        xp_needed = 100 + (level - 1) * 50
    
    return level


@router.get("/learning/stats/daily")
async def get_daily_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Получить статистику за сегодня"""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Сколько слов выучено сегодня
    words_today_result = await db.execute(
        select(func.count(UserWordProgress.id))
        .where(UserWordProgress.user_id == current_user.id)
        .where(UserWordProgress.last_practiced >= today_start)
        .where(UserWordProgress.times_correct > 0)
    )
    words_today = words_today_result.scalar() or 0
    
    # Цель на сегодня
    daily_goal = current_user.daily_goal
    
    return {
        "words_today": words_today,
        "daily_goal": daily_goal,
        "progress_percent": min(100, int((words_today / daily_goal) * 100)) if daily_goal > 0 else 0,
        "goal_achieved": words_today >= daily_goal
    }