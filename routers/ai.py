"""
Aevi - AI Assistant Router
Файл: app/routers/ai.py
AI-помощник, генерация историй, проверка эссе, перевод, озвучка
Использует DeepSeek API (через OpenRouter)
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import httpx
import json
import base64

from app.config import settings
from app.database.session import get_db
from app.database.models import User, Word, Language
from app.routers.auth import get_current_user

router = APIRouter()

# Модели запросов/ответов
class ChatRequest(BaseModel):
    message: str
    context: Optional[List[Dict[str, str]]] = None  # история диалога
    target_language: Optional[str] = None  # на каком языке общаться

class ChatResponse(BaseModel):
    reply: str
    translation: Optional[str] = None  # перевод ответа на родной язык
    corrected_message: Optional[str] = None  # исправленная версия сообщения пользователя
    corrections: Optional[List[Dict[str, str]]] = None  # list of {"original": "xxx", "corrected": "yyy", "explanation": "zzz"}

class StoryRequest(BaseModel):
    language_code: str
    level: str  # A1, A2, B1, B2, C1
    topic: Optional[str] = None
    length: str = "short"  # short, medium, long

class StoryResponse(BaseModel):
    title: str
    content: str
    translation: Optional[str] = None
    words_to_learn: List[Dict[str, str]] = []

class EssayCheckRequest(BaseModel):
    essay: str
    language_code: str
    level: str

class EssayCheckResponse(BaseModel):
    score: int  # 0-100
    feedback: str
    corrections: List[Dict[str, Any]]
    improved_version: str
    grammar_mistakes: int
    vocabulary_score: int

class TranslationRequest(BaseModel):
    text: str
    from_lang: str
    to_lang: str

class TranslationResponse(BaseModel):
    translated_text: str
    detected_language: Optional[str] = None
    alternative_translations: Optional[List[str]] = None

class TTSRequest(BaseModel):
    text: str
    language_code: str
    voice: Optional[str] = "default"  # male, female, default


# Системные промпты для разных задач
SYSTEM_PROMPTS = {
    "chat_helper": """Ты — Aevi AI, дружелюбный помощник в изучении языков. 
Твоя задача:
1. Отвечать на вопросы пользователя о языке, грамматике, словах
2. Исправлять ошибки пользователя, если он пишет на изучаемом языке
3. Объяснять правила простым языком
4. Подбадривать и мотивировать
5. Адаптировать сложность ответа под уровень пользователя

Будь полезным, но не слишком многословным. Используй эмодзи для дружелюбности.""",

    "story_generator": """Ты — писатель, создающий короткие истории для изучения языка.
Правила:
1. Используй простые слова и короткие предложения
2. История должна быть интересной и запоминающейся
3. Включи в историю 5-10 новых слов (выдели их жирным)
4. После истории дай список новых слов с переводом
5. Адаптируй сложность под уровень пользователя (A1, A2, B1, B2, C1)""",

    "essay_checker": """Ты — эксперт по языку, проверяющий эссе.
Для каждого эссе:
1. Оцени по 100-балльной шкале
2. Найди грамматические ошибки и предложи исправления
3. Оцени словарный запас (насколько разнообразные слова)
4. Напиши общую обратную связь (1-2 абзаца)
5. Предложи улучшенную версию эссе

Формат ответа: JSON с полями score, feedback, corrections, improved_version"""
}


async def call_deepseek_api(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    """Вызов DeepSeek API через OpenRouter"""
    if not settings.OPENROUTER_API_KEY:
        raise HTTPException(status_code=503, detail="AI service not configured")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.OPENROUTER_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1000
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"AI API error: {response.text}"
            )
        
        data = response.json()
        return data["choices"][0]["message"]["content"]


@router.post("/ai/chat", response_model=ChatResponse)
async def ai_chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Чат с AI-помощником
    Можно общаться на изучаемом языке, AI будет исправлять ошибки
    """
    target_lang = request.target_language or current_user.current_language
    
    # Получаем название языка
    lang_result = await db.execute(
        select(Language).where(Language.code == target_lang)
    )
    language = lang_result.scalar_one_or_none()
    lang_name = language.name if language else target_lang
    
    # Определяем уровень пользователя для этого языка
    # TODO: получить реальный уровень пользователя
    user_level = "A2"
    
    # Формируем системный промпт
    system_prompt = f"""{SYSTEM_PROMPTS['chat_helper']}

Пользователь изучает {lang_name}, уровень ~{user_level}.

Если пользователь пишет на {lang_name}:
1. Ответь на том же языке
2. Если есть ошибки, мягко исправь их
3. Дай краткое объяснение ошибки

Если пользователь пишет на русском — отвечай тоже пояснениями на русском, но примеры давай на {lang_name}.

Твой ответ должен быть полезным, дружелюбным и мотивирующим."""
    
    # Собираем историю диалога
    messages = [{"role": "system", "content": system_prompt}]
    
    if request.context:
        messages.extend(request.context)
    
    messages.append({"role": "user", "content": request.message})
    
    # Получаем ответ от AI
    try:
        ai_reply = await call_deepseek_api(messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")
    
    # Проверяем, нужно ли исправлять сообщение пользователя
    corrections = None
    corrected_message = None
    
    # Если пользователь писал на изучаемом языке, запросим исправление
    if request.target_language:
        correction_prompt = f"""
Проанализируй сообщение пользователя на {lang_name}:
"{request.message}"

Если есть ошибки, верни JSON:
{{
    "corrected": "исправленная версия",
    "corrections": [
        {{"original": "ошибочная фраза", "corrected": "правильно", "explanation": "почему так"}}
    ]
}}

Если ошибок нет, верни: {{"corrected": null, "corrections": []}}
"""
        
        try:
            correction_response = await call_deepseek_api([
                {"role": "system", "content": correction_prompt},
                {"role": "user", "content": request.message}
            ], temperature=0.3)
            
            # Парсим JSON
            import re
            json_match = re.search(r'\{.*\}', correction_response, re.DOTALL)
            if json_match:
                correction_data = json.loads(json_match.group())
                corrected_message = correction_data.get("corrected")
                corrections = correction_data.get("corrections", [])
        except:
            pass  # Не показываем ошибку пользователю, просто пропускаем исправления
    
    # Переводим ответ, если нужно
    translation = None
    if target_lang != "ru" and current_user.current_language == "ru":
        # Переводим ответ AI на русский для понимания
        try:
            translation_response = await call_deepseek_api([
                {"role": "system", "content": f"Переведи следующий текст с {lang_name} на русский. Только перевод, без комментариев."},
                {"role": "user", "content": ai_reply}
            ], temperature=0.3)
            translation = translation_response
        except:
            pass
    
    return ChatResponse(
        reply=ai_reply,
        translation=translation,
        corrected_message=corrected_message,
        corrections=corrections
    )


@router.post("/ai/story", response_model=StoryResponse)
async def generate_story(
    request: StoryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Сгенерировать историю на изучаемом языке
    """
    # Получаем язык
    lang_result = await db.execute(
        select(Language).where(Language.code == request.language_code)
    )
    language = lang_result.scalar_one_or_none()
    
    if not language:
        raise HTTPException(status_code=404, detail=f"Language {request.language_code} not found")
    
    # Длина истории
    length_map = {"short": "~200 слов", "medium": "~400 слов", "long": "~600 слов"}
    length_desc = length_map.get(request.length, "~200 слов")
    
    topic_desc = request.topic if request.topic else "повседневная жизнь"
    
    prompt = f"""
Создай короткую историю на {language.name} для изучения языка.
Уровень: {request.level}
Тема: {topic_desc}
Длина: {length_desc}

Требования:
1. Используй слова, подходящие для уровня {request.level}
2. Выдели новые или важные слова знаком **вот так**
3. История должна быть интересной и иметь смысл
4. После истории дай список новых слов с переводом на русский

Формат ответа:
ЗАГОЛОВОК: [название истории]

[текст истории со **выделенными** словами]

НОВЫЕ СЛОВА:
- **слово1** — перевод
- **слово2** — перевод
...
"""
    
    try:
        ai_response = await call_deepseek_api([
            {"role": "system", "content": SYSTEM_PROMPTS["story_generator"]},
            {"role": "user", "content": prompt}
        ], temperature=0.8)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")
    
    # Парсим ответ
    import re
    
    # Извлекаем заголовок
    title_match = re.search(r'ЗАГОЛОВОК:\s*(.+?)(?:\n|$)', ai_response)
    title = title_match.group(1).strip() if title_match else "Новая история"
    
    # Извлекаем историю (всё между заголовком и НОВЫЕ СЛОВА)
    content_match = re.search(r'(?:ЗАГОЛОВОК:.*?\n)(.+?)(?=\nНОВЫЕ СЛОВА|\n*$)', ai_response, re.DOTALL)
    content = content_match.group(1).strip() if content_match else ai_response
    
    # Извлекаем новые слова
    words_match = re.search(r'НОВЫЕ СЛОВА:\n(.*)', ai_response, re.DOTALL)
    words_to_learn = []
    
    if words_match:
        words_text = words_match.group(1)
        word_matches = re.findall(r'\*\*(.+?)\*\*\s*[—\-]\s*(.+)', words_text)
        for word, translation in word_matches:
            words_to_learn.append({"word": word.strip(), "translation": translation.strip()})
    
    # Генерируем перевод на русский
    translation = None
    try:
        translation_response = await call_deepseek_api([
            {"role": "system", "content": f"Переведи следующий текст с {language.name} на русский. Сохрани смысл и стиль."},
            {"role": "user", "content": content[:1500]}  # ограничиваем длину
        ], temperature=0.3)
        translation = translation_response
    except:
        pass
    
    return StoryResponse(
        title=title,
        content=content,
        translation=translation,
        words_to_learn=words_to_learn[:10]
    )


@router.post("/ai/check-essay", response_model=EssayCheckResponse)
async def check_essay(
    request: EssayCheckRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Проверить эссе на изучаемом языке
    """
    # Получаем название языка
    lang_map = {
        "en": "английский", "es": "испанский", "de": "немецкий",
        "fr": "французский", "th": "тайский", "zh": "китайский",
        "ja": "японский", "ko": "корейский"
    }
    lang_name = lang_map.get(request.language_code, request.language_code)
    
    prompt = f"""
Проверь эссе на {lang_name} (уровень пользователя: {request.level}):

ЭССЕ:
{request.essay}

Верни ТОЛЬКО JSON в формате:
{{
    "score": 85,
    "feedback": "Общая обратная связь (на русском)",
    "corrections": [
        {{"original": "ошибочная фраза", "corrected": "исправление", "explanation": "почему ошибка"}}
    ],
    "improved_version": "улучшенная версия эссе",
    "grammar_mistakes": 3,
    "vocabulary_score": 75
}}
"""
    
    try:
        ai_response = await call_deepseek_api([
            {"role": "system", "content": SYSTEM_PROMPTS["essay_checker"]},
            {"role": "user", "content": prompt}
        ], temperature=0.4)
        
        # Извлекаем JSON
        import re
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON in response")
        
        data = json.loads(json_match.group())
        
        return EssayCheckResponse(
            score=data.get("score", 70),
            feedback=data.get("feedback", "Эссе требует доработки"),
            corrections=data.get("corrections", []),
            improved_version=data.get("improved_version", request.essay),
            grammar_mistakes=data.get("grammar_mistakes", 0),
            vocabulary_score=data.get("vocabulary_score", 50)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Essay check failed: {str(e)}")


@router.post("/ai/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Перевести текст с одного языка на другой
    """
    # Карта кодов языков в названия
    language_names = {
        "en": "English", "ru": "Russian", "es": "Spanish",
        "de": "German", "fr": "French", "th": "Thai",
        "zh": "Chinese", "ja": "Japanese", "ko": "Korean"
    }
    
    from_name = language_names.get(request.from_lang, request.from_lang)
    to_name = language_names.get(request.to_lang, request.to_lang)
    
    prompt = f"""
Переведи следующий текст с {from_name} на {to_name}:

{request.text}

Верни ТОЛЬКО JSON:
{{
    "translation": "переведённый текст",
    "alternatives": ["альтернативный перевод 1", "альтернативный перевод 2"]
}}
"""
    
    try:
        ai_response = await call_deepseek_api([
            {"role": "system", "content": "Ты — профессиональный переводчик. Переводи точно, сохраняя смысл и стиль."},
            {"role": "user", "content": prompt}
        ], temperature=0.3)
        
        import re
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return TranslationResponse(
                translated_text=data.get("translation", "Ошибка перевода"),
                detected_language=request.from_lang,
                alternative_translations=data.get("alternatives", [])
            )
        
        return TranslationResponse(
            translated_text=ai_response[:500],
            detected_language=request.from_lang
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.post("/ai/tts")
async def text_to_speech(
    request: TTSRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Текст в речь (озвучка слов и фраз)
    """
    # Если нет ElevenLabs API, возвращаем заглушку
    if not settings.ELEVENLABS_API_KEY:
        # Используем бесплатный TTS от DeepSeek? У них нет.
        # Возвращаем информацию, что нужно настроить API
        raise HTTPException(
            status_code=501,
            detail="TTS service not configured. Set ELEVENLABS_API_KEY in .env"
        )
    
    # Маппинг языков на голоса ElevenLabs
    voice_map = {
        "en": "21m00Tcm4TlvDq8ikWAM",  # Rachel
        "es": "EXAVITQu4L4MjE1Gz3nD",  # Antonio
        "de": "VR6A2WLikK3wQn6lD1Qa",  # Thomas
        "fr": "ThT5KcEGYP6aN1T3kC9a",  # Remy
        "ja": "AZnzlk1XvdvUeBnXmlld",  # Elli
        "zh": "EXAVITQu4L4MjE1Gz3nD",  # default
    }
    
    voice_id = voice_map.get(request.language_code, "21m00Tcm4TlvDq8ikWAM")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": settings.ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": request.text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="TTS generation failed"
            )
        
        # Возвращаем аудио в base64
        audio_base64 = base64.b64encode(response.content).decode()
        
        return {
            "audio_base64": audio_base64,
            "format": "mp3",
            "text": request.text,
            "language": request.language_code
        }


@router.get("/ai/suggest-word")
async def suggest_word(
    language_code: str,
    topic: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    AI предлагает слово для изучения по теме
    """
    lang_result = await db.execute(
        select(Language).where(Language.code == language_code)
    )
    language = lang_result.scalar_one_or_none()
    
    if not language:
        raise HTTPException(status_code=404, detail=f"Language {language_code} not found")
    
    topic_desc = topic if topic else "повседневная жизнь"
    
    prompt = f"""
Предложи одно интересное слово на {language.name} для изучения.
Тема: {topic_desc}
Уровень пользователя: A2-B1

Верни ТОЛЬКО JSON:
{{
    "word": "слово на {language.name}",
    "translation": "перевод на русский",
    "transcription": "транскрипция (если применимо)",
    "example": "пример использования на {language.name}",
    "example_translation": "перевод примера",
    "why_interesting": "почему это слово полезно выучить (1 предложение)"
}}
"""
    
    try:
        ai_response = await call_deepseek_api([
            {"role": "system", "content": "Ты — языковой эксперт, помогающий расширять словарный запас."},
            {"role": "user", "content": prompt}
        ], temperature=0.8)
        
        import re
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        
        return {"error": "Failed to generate word suggestion"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))