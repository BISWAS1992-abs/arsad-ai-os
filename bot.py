from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from config import TELEGRAM_BOT_TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Assalamu Alaikum!\n\nWelcome to Arsad AI OS.\nআমি প্রস্তুত। খুব শীঘ্রই আমি Gemini AI-এর সাথে কথা বলতে পারব।"
    )


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("✅ Arsad AI OS Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
