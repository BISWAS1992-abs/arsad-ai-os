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
    save_goal,
    get_goal,
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

    loading = await update.message.reply_text(
        "🤔 আপনার প্রশ্নটি বিশ্লেষণ করছি..."
    )

    try:
        add_user(user_id)

        # =========================
        # NAME MEMORY
        # =========================

        if user_message.lower() in [
            "আমার নাম কি",
            "আমার নাম কী",
            "আমার নাম কি?",
            "আমার নাম কী?",
            "আমার নাম?",
        ]:

            name = get_name(user_id)

            if name:
                await loading.edit_text(f"😊 আপনার নাম {name}।")
            else:
                await loading.edit_text(
                    "🙂 আমি এখনও আপনার নাম জানি না।\n\nউদাহরণ:\nআমার নাম আরসাদ"
                )

            return

        if user_message.startswith("আমার নাম "):

            name = user_message.replace("আমার নাম", "", 1).strip()

            if name.lower() not in ["কি", "কী", "কি?", "কী?"]:

                save_name(user_id, name)

                await loading.edit_text(
                    f"😊 ঠিক আছে। আমি মনে রাখলাম।\n\nআপনার নাম {name}।"
                )

                return

        # =========================
        # GOAL MEMORY
        # =========================

        if user_message.lower() in [
            "আমার লক্ষ্য কি",
            "আমার লক্ষ্য কী",
            "আমার লক্ষ্য কি?",
            "আমার লক্ষ্য কী?",
        ]:

            goal = get_goal(user_id)

            if goal:
                await loading.edit_text(
                    f"🎯 আপনার লক্ষ্য:\n{goal}"
                )
            else:
                await loading.edit_text(
                    "🙂 আপনি এখনও কোনো লক্ষ্য সংরক্ষণ করেননি।\n\nউদাহরণ:\nআমার লক্ষ্য AI শেখা"
                )

            return

        if user_message.startswith("আমার লক্ষ্য "):

            goal = user_message.replace("আমার লক্ষ্য", "", 1).strip()

            if goal.lower() not in ["কি", "কী", "কি?", "কী?"]:

                save_goal(user_id, goal)

                await loading.edit_text(
                    f"🎯 ঠিক আছে। আমি মনে রাখলাম।\n\nআপনার লক্ষ্য:\n{goal}"
                )

                return

        # =========================
        # GEMINI
        # =========================

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
