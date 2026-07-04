from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from core.ai_engine import ask_gemini
from core.memory import init_db

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 আসসালামু আলাইকুম!\n\n"
        "আমি Arsad AI OS.\n"
        "আপনার AI Assistant।"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Loading Message
    loading = await update.message.reply_text(
        "🤔 আপনার প্রশ্নটি বিশ্লেষণ করছি..."
    )

    try:
        reply = ask_gemini(user_message)

        # Loading Message Edit হবে
        await loading.edit_text(reply)

    except Exception as e:
        print(f"Error: {e}")

        await loading.edit_text(
            "❌ সাময়িকভাবে AI Service পাওয়া যাচ্ছে না। অনুগ্রহ করে একটু পরে আবার চেষ্টা করুন।"
        )
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Arsad AI OS Started Successfully")

    app.run_polling()


if __name__ == "__main__":
    main()
