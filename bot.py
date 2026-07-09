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
from core.memory import (
    init_db,
    add_user,
    save_name,
    get_name,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    add_user(user_id)

    await update.message.reply_text(
        "🤖 আসসালামু আলাইকুম!\n\n"
        "আমি Arsad AI OS.\n"
        "আপনার AI Assistant।"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text.strip()

    # Loading Message
    loading = await update.message.reply_text(
        "🤔 আপনার প্রশ্নটি বিশ্লেষণ করছি..."
    )

    try:
        # User Add
        add_user(user_id)

        # নাম সংরক্ষণ
        if user_message.startswith("আমার নাম "):
            name = user_message.replace("আমার নাম", "").strip()

            save_name(user_id, name)

            await loading.edit_text(
                f"😊 ঠিক আছে। আমি মনে রাখলাম।\n\nআপনার নাম {name}।"
            )
            return

        # নাম জিজ্ঞেস করলে
        if user_message in [
            "আমার নাম কি",
            "আমার নাম কী",
            "আমার নাম?",
        ]:
            name = get_name(user_id)

            if name:
                await loading.edit_text(
                    f"😊 আপনার নাম {name}।"
                )
            else:
                await loading.edit_text(
                    "আমি এখনও আপনার নাম জানি না।\n\nআপনি লিখুন:\nআমার নাম আরসাদ"
                )

            return

        # Gemini উত্তর
        reply = ask_gemini(user_message)

        await loading.edit_text(reply)

    except Exception as e:
        print(f"Error: {e}")

        await loading.edit_text(
            "❌ সাময়িকভাবে AI Service পাওয়া যাচ্ছে না। অনুগ্রহ করে একটু পরে আবার চেষ্টা করুন।"
        )


def main():
    init_db()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("✅ Arsad AI OS Started Successfully")

    app.run_polling()


if __name__ == "__main__":
    main()
