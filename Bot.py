import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import json
import random
import ScrapingAnekdots

def load_anekdots_list():
    try:
        json_list = list()
        with open("anekdots.json", encoding="utf-8") as f:
            f_json = json.load(f)
            for x in range(0, len(f_json)):
                json_list.append(f_json[x]["joke"])
        return json_list
    except FileNotFoundError:
        print("anekdots.json - > Ошибка: Файл не найден.")
        return []
    except PermissionError:
        print("anekdots.json - > Ошибка: Нет прав доступа к файлу.")
        return []
    except IsADirectoryError:
        print("anekdots.json - > Ошибка: Указанный путь является директорией.")
        return []
    except OSError as e:
        print(f"anekdots.json - > Ошибка: Ошибка ввода-вывода: {e}")
        return []
    except json.JSONDecodeError:
        print("Ошибка: файл anekdots.json содержит некорректный JSON")
        return []
json_list = load_anekdots_list()

# Логи для отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ← Вставь свой реальный токен
TOKEN = "8377899563:AAF1gua_s3jvxPA1-lRueR2fCIIPscml8gE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я самый простой бот 😄\n"
        "Напиши мне что-нибудь — я отвечу!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я умею:\n"
        "/start — начать\n"
        "/help — эта подсказка\n"
        "и просто болтать 😎"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "привет" in text or "здравствуй" in text:
        answer = "Привет-привет! Как дела?"
    elif "как дела" in text:
        answer = "У меня огонь, а у тебя? 🚀"
    elif "пока" in text:
        answer = "Пока-пока! Заходи ещё 😄"
    elif "блинчик" in text:
        answer = "Так ты захотел поесть? могу дать вуксный рецепт! Cделаешь их за 15 минут до еды:)\n" \
                 "Ингредиенты \n" \
                    "1. молоко 500 мл\n" \
                    "2. яйца 3 шт.\n" \
                    "3. мука 200 г\n" \
                    "4. масло сливочное (или растительное) 30 г (2 ст. ложки)\n" \
                    "5. сахар 30 г (2 ст. ложки)\n" \
                    "соль 2-3 г (1/2 ч. ложки)"
    elif "анекдот" or "разсмеши" or "розсмеши меня" or "дай дульку" or "мне скучно" in text:
        if len(json_list):
            rand_int = random.randint(0, len(json_list)-1)
            answer = "Минута смеха:\n" + json_list[rand_int]
        else:
            answer = "Сори.. Пока не могу ничего придумать..."

    else:
        answer = f"Ты написал: {update.message.text}\nЯ пока простой, но учусь 😅"

    await update.message.reply_text(answer)


def main():  # ← обычная (не async) функция!
    app = Application.builder().token(TOKEN).build()
    json_list = load_anekdots_list()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    json_anekdots = ScrapingAnekdots.parse_anekdotov_month()
    print("Бот запускается... (Ctrl+C для остановки)")
     #Запускаем polling — БЕЗ await, потому что main не асинхронная
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True   # ← полезно при перезапусках
    )


if __name__ == "__main__":
    main()  # ← просто вызываем обычную функцию