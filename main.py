
import os
import logging
from telegram import (
    Update, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

news = []
clubs = []
schedule = "Jadval hali kiritilmagan."
requests = []

MENU = [
    ["🏫 Maktab haqida", "🎯 To‘garaklar"],
    ["📅 Jadval", "📝 To‘garakka yozilish"],
    ["📢 Yangiliklar", "☎️ Bog‘lanish"],
]

def is_admin(update):
    return (
        ADMIN_ID
        and ADMIN_ID.isdigit()
        and update.effective_user
        and update.effective_user.id == int(ADMIN_ID)
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("action", None)
    keyboard = ReplyKeyboardMarkup(MENU, resize_keyboard=True)
    await update.message.reply_text(
        "🏫 Angren shahri 25-maktab botiga xush kelibsiz!\n"
        "Kerakli bo‘limni tanlang.",
        reply_markup=keyboard
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("⛔ Bu bo‘lim faqat administrator uchun.")
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Yangilik qo‘shish", callback_data="news")],
        [InlineKeyboardButton("🎯 To‘garak qo‘shish", callback_data="club")],
        [InlineKeyboardButton("📅 Jadvalni o‘zgartirish", callback_data="schedule")],
        [InlineKeyboardButton("📝 Yozilish so‘rovlari", callback_data="requests")],
        [InlineKeyboardButton("📋 To‘garaklarni ko‘rish", callback_data="clubs")],
    ])
    await update.message.reply_text("🔐 ADMIN PANEL\n\nKerakli amalni tanlang:", reply_markup=keyboard)

async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(update):
        await query.edit_message_text("⛔ Ruxsat yo‘q.")
        return

    action = query.data

    if action == "requests":
        if not requests:
            await query.edit_message_text("Hozircha yozilish so‘rovlari yo‘q.")
        else:
            result = "\n\n".join(requests[-20:])
            await query.edit_message_text("📝 SO‘ROVLAR:\n\n" + result[:4000])
        return

    if action == "clubs":
        result = "\n".join("• " + c for c in clubs) or "Hozircha to‘garak qo‘shilmagan."
        await query.edit_message_text("🎯 TO‘GARAKLAR:\n\n" + result[:4000])
        return

    prompts = {
        "news": ("news", "📢 E'lon qilinadigan yangilik matnini yubor:"),
        "club": ("club", "🎯 To‘garak nomi va ma'lumotlarini yubor:"),
        "schedule": ("schedule", "📅 Yangi jadvalni yubor:")
    }

    if action in prompts:
        context.user_data["action"] = prompts[action][0]
        await query.edit_message_text(prompts[action][1])

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    action = context.user_data.get("action")

    if action and is_admin(update):
        context.user_data.pop("action", None)

        if action == "news":
            news.append(text)
            await update.message.reply_text("✅ Yangilik qo‘shildi!")

        elif action == "club":
            clubs.append(text)
            await update.message.reply_text("✅ To‘garak qo‘shildi!")

        elif action == "schedule":
            global schedule
            schedule = text
            await update.message.reply_text("✅ Jadval yangilandi!")

        return

    if action == "register":
        context.user_data.pop("action", None)
        requests.append(
            f"Foydalanuvchi ID: {update.effective_user.id}\n"
            f"To‘garak: {text}"
        )

        if ADMIN_ID and ADMIN_ID.isdigit():
            try:
                await context.bot.send_message(
                    chat_id=int(ADMIN_ID),
                    text="📝 Yangi yozilish so‘rovi:\n"
                         f"Foydalanuvchi ID: {update.effective_user.id}\n"
                         f"To‘garak: {text}"
                )
            except Exception:
                logging.exception("Administratorga xabar yuborilmadi")

        await update.message.reply_text("✅ So‘rovingiz qabul qilindi!")
        return

    if text == "🏫 Maktab haqida":
        answer = "🏫 Angren shahri 25-maktab axborot boti."
    elif text == "🎯 To‘garaklar":
        answer = "🎯 TO‘GARAKLAR:\n" + (
            "\n".join("• " + c for c in clubs)
            if clubs else "To‘garaklar ma'lumoti hali kiritilmagan."
        )
    elif text == "📅 Jadval":
        answer = "📅 JADVAL:\n" + schedule
    elif text == "📝 To‘garakka yozilish":
        context.user_data["action"] = "register"
        answer = "Qaysi to‘garakka yozilmoqchisiz? Nomini yuboring."
    elif text == "📢 Yangiliklar":
        answer = "📢 MAKTAB YANGILIKLARI:\n" + (
            "\n\n".join(news[-10:])
            if news else "Hozircha yangilik yo‘q."
        )
    elif text == "☎️ Bog‘lanish":
        answer = "☎️ Maktabning rasmiy aloqa ma'lumotlari keyin kiritiladi."
    else:
        answer = "Menyudagi bo‘limlardan birini tanlang."

    await update.message.reply_text(answer)

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN sozlanmagan!")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(admin_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
    
