from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from core.ai_engine import ask_gemini


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 আসসালামু আলাইকুম!\n\nআমি Arsad AI OS.\nআপনার AI Assistant।"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        reply = ask_gemini(user_message)
        await update.message.reply_text(reply)

    except Exception:
        await update.message.reply_text(
            "❌ দুঃখিত, এখন উত্তর দিতে পারছি না। পরে আবার চেষ্টা করুন।"
        )


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Arsad AI OS Started")

    app.run_polling()


if __name__ == "__main__":
    main()
