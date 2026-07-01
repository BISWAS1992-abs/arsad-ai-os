import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Telegram Bot Token not found")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key not found")
