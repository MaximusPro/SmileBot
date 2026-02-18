import requests
import re
import json
from datetime import datetime

def clean_joke(text: str) -> str:
    """
    Убирает мусор в начале и конце шутки:
    - /опубликован ... /
    - даты в начале
    - лишние переносы строк
    - нормализует тире
    """
    if not text:
        return ""

    # Убираем начальный блок вида /опубликован ... /
    text = re.sub(r'^/опубликован\s*.*?\n*/\s*', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Убираем возможные остатки дат в начале (20 января, 28 января и т.п.)
    text = re.sub(r'^(?:\d{1,2}\s*(?:января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s*)', '', text, flags=re.IGNORECASE)

    # Убираем лишние переносы строк в начале и конце
    text = text.strip()

    # Нормализуем тире (— вместо разных вариантов)
    text = re.sub(r'\s*[-–—−]\s*', ' — ', text)

    # Убираем множественные пустые строки внутри текста
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'&mdash;', '-', text)
    # Финальная обрезка
    return text.strip()
def parse_anekdotov_month():
    url = "https://anekdotov.net/anekdot/month/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return []

    text = response.text

    # Удаляем HTML-теги → заменяем на перенос строки
    clean_text = re.sub(r'<[^>]+>', '\n', text)

    # Нормализуем переносы строк
    clean_text = re.sub(r'\s*\n\s*', '\n', clean_text)
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
    clean_text = clean_text.strip()

    # Основной паттерн: захватываем место, дату и блок анекдота до следующего места
    pattern = r'(\d+)\s*место\s*[:.]?\s*(?:опубликован\s*\[([^\]]+)\])?\s*(.*?)(?=\d+\s*место|\Z)'
    matches = re.findall(pattern, clean_text, re.DOTALL | re.IGNORECASE)

    anekdots = []

    for place_str, published, raw_content in matches:
        place = int(place_str.strip())
        published = (published or "").strip()

        # === Очень тщательная очистка анекдота ===
        joke = raw_content.strip()

        # 1. Убираем markdown-ссылки → оставляем только текст внутри
        joke = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', joke)

        # 2. Убираем рейтинг в конце (в любом виде)
        joke = re.sub(r'\|\s*-2\s+-1\s+0\s+\+1\s+\+2\s*\|.*', '', joke, flags=re.DOTALL)
        joke = re.sub(r'-2\s+-1\s+0\s+\+1\s+\+2.*', '', joke, flags=re.DOTALL)

        # 3. Убираем возможные остатки навигации, кнопок, разделителей
        joke = re.sub(r'(?:\*{3,}|-{3,}|={3,}).*', '', joke, flags=re.DOTALL)
        joke = re.sub(r'(?:Голосовать|Рейтинг|Комментарии).*', '', joke, flags=re.IGNORECASE | re.DOTALL)

        # 4. Убираем лишние строки в начале и конце (часто остаются даты или метки)
        joke = re.sub(r'^[\s\n]*(?:опубликован.*|место.*|\d+\s+февраля.*)[\s\n]*', '', joke,
                      flags=re.IGNORECASE | re.MULTILINE)
        joke = re.sub(r'[\s\n]*(?:место|Голосовать|Рейтинг).*?$', '', joke, flags=re.IGNORECASE | re.DOTALL)

        # 5. Нормализуем тире в диалогах (— вместо - или --)
        joke = re.sub(r'\s*[-–—]\s*', ' — ', joke)

        # 6. Убираем множественные пустые строки внутри
        joke = re.sub(r'\n{3,}', '\n\n', joke)
        joke = joke.strip()
        joke = clean_joke(joke)
        if not joke or len(joke) < 10:  # минимальная защита от пустышек
            continue

        anekdots.append({
            "place": place,
            "joke": joke,
            "published": published,
            "rating": "-2 -1 0 +1 +2"
        })

    # Сортируем от 15 к 1 (как принято показывать в топе)
    anekdots.sort(key=lambda x: x["place"], reverse=True)

    if anekdots:
        filename = "anekdots.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(anekdots, f, ensure_ascii=False, indent=2)
        print(f"Сохранено {len(anekdots)} чистых анекдотов в {filename}")
    else:
        print("Не удалось извлечь анекдоты — возможно, структура сайта изменилась.")

    return anekdots

