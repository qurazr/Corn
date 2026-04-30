"""
Aevi - Seed Database
Файл: app/database/seed_data.py
Наполняет БД начальными данными: слова, уроки, достижения, товары
Запуск: python -m app.database.seed_data
"""

import asyncio
import json
from datetime import datetime
from sqlalchemy import select
from app.database.session import async_session_maker, init_db
from app.database.models import (
    Language, Word, Lesson, Achievement, ShopItem, 
    DailyTask, Base
)

# ============================================================
# БАЗОВЫЕ СЛОВА ДЛЯ КАЖДОГО ЯЗЫКА (первые 50-100 слов)
# ============================================================

WORDS_BY_LANGUAGE = {
    "en": [  # English - A1 уровень
        {"word": "hello", "translation": "привет", "transcription": "həˈləʊ", "topic": "greetings", "level": "A1", "part_of_speech": "interjection"},
        {"word": "goodbye", "translation": "до свидания", "transcription": "ɡʊdˈbaɪ", "topic": "greetings", "level": "A1", "part_of_speech": "interjection"},
        {"word": "please", "translation": "пожалуйста", "transcription": "pliːz", "topic": "greetings", "level": "A1", "part_of_speech": "adverb"},
        {"word": "thank you", "translation": "спасибо", "transcription": "θæŋk juː", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "yes", "translation": "да", "transcription": "jes", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "no", "translation": "нет", "transcription": "nəʊ", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "cat", "translation": "кот", "transcription": "kæt", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "dog", "translation": "собака", "transcription": "dɒɡ", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "house", "translation": "дом", "transcription": "haʊs", "topic": "home", "level": "A1", "part_of_speech": "noun"},
        {"word": "car", "translation": "машина", "transcription": "kɑː", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
        {"word": "water", "translation": "вода", "transcription": "ˈwɔːtə", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        {"word": "food", "translation": "еда", "transcription": "fuːd", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        {"word": "love", "translation": "любовь", "transcription": "lʌv", "topic": "emotions", "level": "A1", "part_of_speech": "noun"},
        {"word": "friend", "translation": "друг", "transcription": "frend", "topic": "people", "level": "A1", "part_of_speech": "noun"},
        {"word": "family", "translation": "семья", "transcription": "ˈfæməli", "topic": "family", "level": "A1", "part_of_speech": "noun"},
        {"word": "work", "translation": "работа", "transcription": "wɜːk", "topic": "work", "level": "A1", "part_of_speech": "noun"},
        {"word": "study", "translation": "учиться", "transcription": "ˈstʌdi", "topic": "education", "level": "A1", "part_of_speech": "verb"},
        {"word": "happy", "translation": "счастливый", "transcription": "ˈhæpi", "topic": "emotions", "level": "A1", "part_of_speech": "adjective"},
        {"word": "sad", "translation": "грустный", "transcription": "sæd", "topic": "emotions", "level": "A1", "part_of_speech": "adjective"},
        {"word": "big", "translation": "большой", "transcription": "bɪɡ", "topic": "adjectives", "level": "A1", "part_of_speech": "adjective"},
        {"word": "small", "translation": "маленький", "transcription": "smɔːl", "topic": "adjectives", "level": "A1", "part_of_speech": "adjective"},
        {"word": "red", "translation": "красный", "transcription": "red", "topic": "colors", "level": "A1", "part_of_speech": "adjective"},
        {"word": "blue", "translation": "синий", "transcription": "bluː", "topic": "colors", "level": "A1", "part_of_speech": "adjective"},
        {"word": "green", "translation": "зелёный", "transcription": "ɡriːn", "topic": "colors", "level": "A1", "part_of_speech": "adjective"},
        {"word": "one", "translation": "один", "transcription": "wʌn", "topic": "numbers", "level": "A1", "part_of_speech": "numeral"},
        {"word": "two", "translation": "два", "transcription": "tuː", "topic": "numbers", "level": "A1", "part_of_speech": "numeral"},
        {"word": "three", "translation": "три", "transcription": "θriː", "topic": "numbers", "level": "A1", "part_of_speech": "numeral"},
    ],
    
    "es": [  # Español - A1 уровень
        {"word": "hola", "translation": "привет", "transcription": "ˈola", "topic": "greetings", "level": "A1", "part_of_speech": "interjection"},
        {"word": "adiós", "translation": "до свидания", "transcription": "aˈðjos", "topic": "greetings", "level": "A1", "part_of_speech": "interjection"},
        {"word": "por favor", "translation": "пожалуйста", "transcription": "poɾ faˈβoɾ", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "gracias", "translation": "спасибо", "transcription": "ˈɡɾasjas", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "sí", "translation": "да", "transcription": "si", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "no", "translation": "нет", "transcription": "no", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "gato", "translation": "кот", "transcription": "ˈɡato", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "perro", "translation": "собака", "transcription": "ˈpero", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "casa", "translation": "дом", "transcription": "ˈkasa", "topic": "home", "level": "A1", "part_of_speech": "noun"},
        {"word": "coche", "translation": "машина", "transcription": "ˈkotʃe", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
        {"word": "agua", "translation": "вода", "transcription": "ˈaɣwa", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        {"word": "comida", "translation": "еда", "transcription": "koˈmiða", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        {"word": "amor", "translation": "любовь", "transcription": "aˈmoɾ", "topic": "emotions", "level": "A1", "part_of_speech": "noun"},
        {"word": "amigo", "translation": "друг", "transcription": "aˈmiɣo", "topic": "people", "level": "A1", "part_of_speech": "noun"},
        {"word": "familia", "translation": "семья", "transcription": "faˈmilja", "topic": "family", "level": "A1", "part_of_speech": "noun"},
    ],
    
    "de": [  # Deutsch - A1 уровень
        {"word": "hallo", "translation": "привет", "transcription": "haˈloː", "topic": "greetings", "level": "A1", "part_of_speech": "interjection"},
        {"word": "auf Wiedersehen", "translation": "до свидания", "transcription": "aʊf ˈviːdɐˌzeːən", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "bitte", "translation": "пожалуйста", "transcription": "ˈbɪtə", "topic": "greetings", "level": "A1", "part_of_speech": "adverb"},
        {"word": "danke", "translation": "спасибо", "transcription": "ˈdaŋkə", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "ja", "translation": "да", "transcription": "jaː", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "nein", "translation": "нет", "transcription": "naɪn", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "Katze", "translation": "кот", "transcription": "ˈkatsə", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "Hund", "translation": "собака", "transcription": "hʊnt", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "Haus", "translation": "дом", "transcription": "haʊs", "topic": "home", "level": "A1", "part_of_speech": "noun"},
        {"word": "Auto", "translation": "машина", "transcription": "ˈaʊto", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
        {"word": "Wasser", "translation": "вода", "transcription": "ˈvasɐ", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        {"word": "Essen", "translation": "еда", "transcription": "ˈɛsən", "topic": "food", "level": "A1", "part_of_speech": "noun"},
    ],
    
    "fr": [  # Français - A1 уровень
        {"word": "bonjour", "translation": "здравствуйте", "transcription": "bɔ̃ʒuʁ", "topic": "greetings", "level": "A1", "part_of_speech": "interjection"},
        {"word": "au revoir", "translation": "до свидания", "transcription": "o ʁəvwaʁ", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "s'il vous plaît", "translation": "пожалуйста", "transcription": "sil vu plɛ", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "merci", "translation": "спасибо", "transcription": "mɛʁsi", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "oui", "translation": "да", "transcription": "wi", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "non", "translation": "нет", "transcription": "nɔ̃", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "chat", "translation": "кот", "transcription": "ʃa", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "chien", "translation": "собака", "transcription": "ʃjɛ̃", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "maison", "translation": "дом", "transcription": "mɛzɔ̃", "topic": "home", "level": "A1", "part_of_speech": "noun"},
        {"word": "voiture", "translation": "машина", "transcription": "vwa tyʁ", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
        {"word": "eau", "translation": "вода", "transcription": "o", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        {"word": "nourriture", "translation": "еда", "transcription": "nu ʁi tyʁ", "topic": "food", "level": "A1", "part_of_speech": "noun"},
    ],
    
    "th": [  # ไทย - A1 уровень
        {"word": "สวัสดี", "translation": "здравствуйте", "transcription": "sà-wàt-dee", "topic": "greetings", "level": "A1", "part_of_speech": "interjection"},
        {"word": "ลาก่อน", "translation": "до свидания", "transcription": "laa-gòn", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "ขอบคุณ", "translation": "спасибо", "transcription": "kòp-kun", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
        {"word": "ใช่", "translation": "да", "transcription": "châi", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "ไม่", "translation": "нет", "transcription": "mâi", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
        {"word": "แมว", "translation": "кот", "transcription": "maew", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "หมา", "translation": "собака", "transcription": "mǎa", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
        {"word": "บ้าน", "translation": "дом", "transcription": "bâan", "topic": "home", "level": "A1", "part_of_speech": "noun"},
        {"word": "รถ", "translation": "машина", "transcription": "rót", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
        {"word": "น้ำ", "translation": "вода", "transcription": "náam", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        {"word": "อาหาร", "translation": "еда", "transcription": "aa-hǎan", "topic": "food", "level": "A1", "part_of_speech": "noun"},
    ],
    
    "zh": {  # 中文 - A1 уровень
        "words": [
            {"word": "你好", "translation": "здравствуйте", "transcription": "nǐ hǎo", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "再见", "translation": "до свидания", "transcription": "zài jiàn", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "谢谢", "translation": "спасибо", "transcription": "xiè xie", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "是", "translation": "да", "transcription": "shì", "topic": "basics", "level": "A1", "part_of_speech": "verb"},
            {"word": "不是", "translation": "нет", "transcription": "bù shì", "topic": "basics", "level": "A1", "part_of_speech": "phrase"},
            {"word": "猫", "translation": "кот", "transcription": "māo", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
            {"word": "狗", "translation": "собака", "transcription": "gǒu", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
            {"word": "房子", "translation": "дом", "transcription": "fáng zi", "topic": "home", "level": "A1", "part_of_speech": "noun"},
            {"word": "车", "translation": "машина", "transcription": "chē", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
            {"word": "水", "translation": "вода", "transcription": "shuǐ", "topic": "food", "level": "A1", "part_of_speech": "noun"},
            {"word": "食物", "translation": "еда", "transcription": "shí wù", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        ]
    },
    
    "ja": {  # 日本語 - A1 уровень
        "words": [
            {"word": "こんにちは", "translation": "здравствуйте", "transcription": "konnichiwa", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "さようなら", "translation": "до свидания", "transcription": "sayōnara", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "ありがとう", "translation": "спасибо", "transcription": "arigatō", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "はい", "translation": "да", "transcription": "hai", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
            {"word": "いいえ", "translation": "нет", "transcription": "īe", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
            {"word": "猫", "translation": "кот", "transcription": "neko", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
            {"word": "犬", "translation": "собака", "transcription": "inu", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
            {"word": "家", "translation": "дом", "transcription": "ie", "topic": "home", "level": "A1", "part_of_speech": "noun"},
            {"word": "車", "translation": "машина", "transcription": "kuruma", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
            {"word": "水", "translation": "вода", "transcription": "mizu", "topic": "food", "level": "A1", "part_of_speech": "noun"},
            {"word": "食べ物", "translation": "еда", "transcription": "tabemono", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        ]
    },
    
    "ko": {  # 한국어 - A1 уровень
        "words": [
            {"word": "안녕하세요", "translation": "здравствуйте", "transcription": "annyeonghaseyo", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "안녕히 가세요", "translation": "до свидания", "transcription": "annyeonghi gaseyo", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "감사합니다", "translation": "спасибо", "transcription": "gamsahamnida", "topic": "greetings", "level": "A1", "part_of_speech": "phrase"},
            {"word": "네", "translation": "да", "transcription": "ne", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
            {"word": "아니요", "translation": "нет", "transcription": "aniyo", "topic": "basics", "level": "A1", "part_of_speech": "adverb"},
            {"word": "고양이", "translation": "кот", "transcription": "goyangi", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
            {"word": "개", "translation": "собака", "transcription": "gae", "topic": "animals", "level": "A1", "part_of_speech": "noun"},
            {"word": "집", "translation": "дом", "transcription": "jip", "topic": "home", "level": "A1", "part_of_speech": "noun"},
            {"word": "차", "translation": "машина", "transcription": "cha", "topic": "transport", "level": "A1", "part_of_speech": "noun"},
            {"word": "물", "translation": "вода", "transcription": "mul", "topic": "food", "level": "A1", "part_of_speech": "noun"},
            {"word": "음식", "translation": "еда", "transcription": "eumsik", "topic": "food", "level": "A1", "part_of_speech": "noun"},
        ]
    }
}

# ============================================================
# УРОКИ ДЛЯ КАЖДОГО ЯЗЫКА
# ============================================================

LESSONS_BY_LANGUAGE = {
    "en": [
        {"title": "Greetings & Introductions", "description": "Learn how to say hello, goodbye, and introduce yourself", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "Family and Friends", "description": "Words for family members and close friends", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
        {"title": "Colors and Numbers", "description": "Basic colors and numbers 1-20", "topic": "basics", "level": "A1", "words_count": 15, "order_index": 3, "xp_reward": 50, "coins_reward": 10},
        {"title": "Food and Drinks", "description": "Common food items and beverages", "topic": "food", "level": "A1", "words_count": 12, "order_index": 4, "xp_reward": 60, "coins_reward": 10},
        {"title": "Animals", "description": "Pets and wild animals", "topic": "animals", "level": "A1", "words_count": 10, "order_index": 5, "xp_reward": 50, "coins_reward": 10},
    ],
    "es": [
        {"title": "Saludos y Presentaciones", "description": "Aprende a saludar y presentarte", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "La Familia", "description": "Palabras para miembros de la familia", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
        {"title": "Colores y Números", "description": "Colores básicos y números", "topic": "basics", "level": "A1", "words_count": 15, "order_index": 3, "xp_reward": 50, "coins_reward": 10},
    ],
    "de": [
        {"title": "Begrüßungen", "description": "Lerne, wie man Hallo sagt", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "Familie", "description": "Familienmitglieder auf Deutsch", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
    ],
    "fr": [
        {"title": "Salutations", "description": "Apprenez à dire bonjour", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "La Famille", "description": "Les membres de la famille", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
    ],
    "th": [
        {"title": "การทักทาย", "description": "เรียนรู้การทักทาย", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "ครอบครัว", "description": "คำศัพท์เกี่ยวกับครอบครัว", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
    ],
    "zh": [
        {"title": "问候", "description": "学习如何打招呼", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "家庭", "description": "家庭成员的词汇", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
    ],
    "ja": [
        {"title": "挨拶", "description": "挨拶の仕方を学ぶ", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "家族", "description": "家族の単語", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
    ],
    "ko": [
        {"title": "인사", "description": "인사하는 방법 배우기", "topic": "greetings", "level": "A1", "words_count": 10, "order_index": 1, "xp_reward": 50, "coins_reward": 10},
        {"title": "가족", "description": "가족 구성원 단어", "topic": "family", "level": "A1", "words_count": 12, "order_index": 2, "xp_reward": 60, "coins_reward": 10},
    ],
}

# ============================================================
# ДОСТИЖЕНИЯ
# ============================================================

ACHIEVEMENTS = [
    {"name": "🌱 Первые шаги", "description": "Выучить первые 10 слов", "icon": "🌱", "xp_reward": 50, "coins_reward": 20, "requirement_type": "words", "requirement_value": 10},
    {"name": "📚 Ученик", "description": "Выучить 50 слов", "icon": "📚", "xp_reward": 100, "coins_reward": 50, "requirement_type": "words", "requirement_value": 50},
    {"name": "🎓 Знаток", "description": "Выучить 200 слов", "icon": "🎓", "xp_reward": 300, "coins_reward": 150, "requirement_type": "words", "requirement_value": 200},
    {"name": "🏆 Полиглот", "description": "Выучить 500 слов", "icon": "🏆", "xp_reward": 500, "coins_reward": 300, "requirement_type": "words", "requirement_value": 500},
    
    {"name": "🔥 7 дней", "description": "Заниматься 7 дней подряд", "icon": "🔥", "xp_reward": 100, "coins_reward": 30, "requirement_type": "streak", "requirement_value": 7},
    {"name": "⚡ 30 дней", "description": "Заниматься 30 дней подряд", "icon": "⚡", "xp_reward": 300, "coins_reward": 100, "requirement_type": "streak", "requirement_value": 30},
    {"name": "💪 100 дней", "description": "Заниматься 100 дней подряд", "icon": "💪", "xp_reward": 1000, "coins_reward": 500, "requirement_type": "streak", "requirement_value": 100},
    
    {"name": "📖 Первый урок", "description": "Завершить первый урок", "icon": "📖", "xp_reward": 50, "coins_reward": 20, "requirement_type": "lessons", "requirement_value": 1},
    {"name": "🎯 10 уроков", "description": "Завершить 10 уроков", "icon": "🎯", "xp_reward": 200, "coins_reward": 80, "requirement_type": "lessons", "requirement_value": 10},
    
    {"name": "⭐ Уровень 5", "description": "Достичь 5 уровня", "icon": "⭐", "xp_reward": 150, "coins_reward": 50, "requirement_type": "level", "requirement_value": 5},
    {"name": "👑 Уровень 10", "description": "Достичь 10 уровня", "icon": "👑", "xp_reward": 300, "coins_reward": 150, "requirement_type": "level", "requirement_value": 10},
    
    {"name": "🤝 Первый друг", "description": "Добавить первого друга", "icon": "🤝", "xp_reward": 50, "coins_reward": 20, "requirement_type": "friends", "requirement_value": 1},
]

# ============================================================
# ЕЖЕДНЕВНЫЕ ЗАДАНИЯ
# ============================================================

DAILY_TASKS = [
    {"title": "📝 Слова дня", "description": "Выучи 10 новых слов", "task_type": "learn_words", "target": 10, "xp_reward": 30, "coins_reward": 10},
    {"title": "📚 Урок дня", "description": "Пройди один урок", "task_type": "complete_lesson", "target": 1, "xp_reward": 40, "coins_reward": 15},
    {"title": "🔥 Поддержи серию", "description": "Занимайся сегодня", "task_type": "streak", "target": 1, "xp_reward": 20, "coins_reward": 5},
    {"title": "🎯 Идеальный урок", "description": "Пройди урок без ошибок", "task_type": "perfect_lesson", "target": 1, "xp_reward": 50, "coins_reward": 20},
    {"title": "⭐ 50 XP", "description": "Набери 50 очков опыта", "task_type": "earn_xp", "target": 50, "xp_reward": 25, "coins_reward": 8},
]

# ============================================================
# ФУНКЦИИ ЗАПОЛНЕНИЯ БД
# ============================================================

async def seed_languages():
    """Заполнение языков"""
    from app.database.models import Language
    
    async with async_session_maker() as session:
        # Проверяем, есть ли уже языки
        result = await session.execute(select(Language))
        existing = result.scalars().first()
        
        if existing:
            print("⚠️ Languages already exist, skipping...")
            return
        
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
        
        for lang_data in languages:
            lang = Language(**lang_data)
            session.add(lang)
        
        await session.commit()
        print("✅ Languages seeded!")


async def seed_words():
    """Заполнение слов"""
    from app.database.models import Language, Word
    
    async with async_session_maker() as session:
        # Получаем все языки
        result = await session.execute(select(Language))
        languages = {lang.code: lang for lang in result.scalars().all()}
        
        for lang_code, words_list in WORDS_BY_LANGUAGE.items():
            if lang_code not in languages:
                continue
            
            lang = languages[lang_code]
            
            # Проверяем, есть ли уже слова для этого языка
            word_result = await session.execute(
                select(Word).where(Word.language_id == lang.id).limit(1)
            )
            if word_result.scalar_one_or_none():
                print(f"⚠️ Words for {lang_code} already exist, skipping...")
                continue
            
            # Добавляем слова
            for word_data in words_list:
                # Если слова в другом формате (для zh, ja, ko)
                if isinstance(word_data, dict):
                    word = Word(
                        language_id=lang.id,
                        word=word_data["word"],
                        translation=word_data["translation"],
                        transcription=word_data.get("transcription", ""),
                        topic=word_data.get("topic", "general"),
                        level=word_data.get("level", "A1"),
                        part_of_speech=word_data.get("part_of_speech", None),
                        example=word_data.get("example", f"This is {word_data['word']}. This is example."),
                        example_translation=word_data.get("example_translation", f"Это {word_data['translation']}. Это пример."),
                        difficulty=1
                    )
                    session.add(word)
            
            await session.commit()
            print(f"✅ Words for {lang_code} seeded ({len(words_list)} words)")


async def seed_lessons():
    """Заполнение уроков"""
    from app.database.models import Language, Lesson
    
    async with async_session_maker() as session:
        result = await session.execute(select(Language))
        languages = {lang.code: lang for lang in result.scalars().all()}
        
        for lang_code, lessons_list in LESSONS_BY_LANGUAGE.items():
            if lang_code not in languages:
                continue
            
            lang = languages[lang_code]
            
            # Проверяем, есть ли уже уроки
            lesson_result = await session.execute(
                select(Lesson).where(Lesson.language_id == lang.id).limit(1)
            )
            if lesson_result.scalar_one_or_none():
                print(f"⚠️ Lessons for {lang_code} already exist, skipping...")
                continue
            
            for lesson_data in lessons_list:
                lesson = Lesson(
                    language_id=lang.id,
                    **lesson_data
                )
                session.add(lesson)
            
            await session.commit()
            print(f"✅ Lessons for {lang_code} seeded ({len(lessons_list)} lessons)")


async def seed_achievements():
    """Заполнение достижений"""
    from app.database.models import Achievement
    
    async with async_session_maker() as session:
        # Проверяем, есть ли уже достижения
        result = await session.execute(select(Achievement).limit(1))
        if result.scalar_one_or_none():
            print("⚠️ Achievements already exist, skipping...")
            return
        
        for ach_data in ACHIEVEMENTS:
            achievement = Achievement(**ach_data)
            session.add(achievement)
        
        await session.commit()
        print(f"✅ Achievements seeded ({len(ACHIEVEMENTS)} achievements)")


async def seed_daily_tasks():
    """Заполнение ежедневных заданий"""
    from app.database.models import DailyTask
    
    async with async_session_maker() as session:
        result = await session.execute(select(DailyTask).limit(1))
        if result.scalar_one_or_none():
            print("⚠️ Daily tasks already exist, skipping...")
            return
        
        for task_data in DAILY_TASKS:
            task = DailyTask(**task_data)
            session.add(task)
        
        await session.commit()
        print(f"✅ Daily tasks seeded ({len(DAILY_TASKS)} tasks)")


async def seed_all():
    """Заполнение всех данных"""
    print("\n🌱 Seeding Aevi database...\n")
    
    await init_db()  # создаём таблицы
    await seed_languages()
    await seed_words()
    await seed_lessons()
    await seed_achievements()
    await seed_daily_tasks()
    
    print("\n✅ Database seeding completed!\n")


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    asyncio.run(seed_all())