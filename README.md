# SmileBot 😄🍳

**Telegram bot for boosting your mood and culinary inspiration**

SmileBot is a fun Telegram bot that:
- sends **fresh jokes** from anekdotov.net
- helps you choose a **dish recipe** for any taste or mood

Made for people who want to smile and eat delicious food at any moment of the day.

## Features

- `/start` — welcome message and list of commands
- `/joke` or just type “joke” / “анекдот” — get a fresh joke from anekdotov.net
- `/food`, `/recipe`, or type “what to cook?” / “что приготовить?” — random recipe or dish ideas
- Supports simple text conversation (you can just write “tell a joke” or “I’m hungry”)

## Technologies

- **Language**: Python 3.10+
- **Telegram library**: aiogram (async) / python-telegram-bot
- **Joke parsing**: requests + BeautifulSoup (module ScrapingAnekdots.py)
- **Recipe source**: (please specify where recipes come from — if parsed or using an API)

## Installation & Running

1. Clone the repository

```bash
git clone https://github.com/MaximusPro/SmileBot.git
cd SmileBot
