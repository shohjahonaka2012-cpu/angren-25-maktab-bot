
import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

MENU = [
    ["🏫 Maktab haqida", "🎯 To‘garaklar"],
    ["📅 Jadval", "📝 To‘garakka yozilish"],
    ["📢 Yangiliklar", "☎️ Bog‘lanish"],
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton(x) for x in row] for row in MENU],
        resize_keyboard=True,
    )
    await update.message.reply_text(
        "Assalomu alaykum!\n"
        "🏫 Angren shahridagi 25-maktab axborot botiga xush kelibsiz!\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=keyboard,
    )

async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    if text == "🏫 Maktab haqida":
        answer = (
            "🏫 ANGREN SHAHRI, 25-MAKTAB\n\n"
            "Maktabimiz haqidagi ma'lumotlar shu bo‘limda "
            "joylashtiriladi."
        )
    elif text == "🎯 To‘garaklar":
        answer = (
            "🎯 MAKTAB TO‘GARAKLARI\n\n"
            "Bu yerga mavjud to‘garaklar va ularning "
            "rahbarlari haqidagi tasdiqlangan ma'lumotlar "
            "kiritiladi."
        )
    elif text == "📅 Jadval":
        answer = (
            "📅 TO‘GARAKLAR JADVALI\n\n"
            "Mashg‘ulot kunlari va vaqtlari maktab "
            "ma'muriyati tasdiqlaganidan so‘ng kiritiladi."
        )
    elif text == "📝 To‘garakka yozilish":
        context.user_data["register"] = True
        await update.message.reply_text(
            "Qaysi to‘garakka yozilmoqchisiz? "
            "To‘garak nomini yuboring."
        )
        return
    elif context.user_data.get("register"):
        context.user_data["register"] = False
        admin_chat = int(ADMIN_ID) if ADMIN_ID and ADMIN_ID.isdigit() else None
        if admin_chat:
            await context.bot.send_message(
                chat_id=admin_chat,
                text=(
                    "📝 Yangi to‘garak so‘rovi\n"
                    f"Foydalanuvchi ID: {update.effective_user.id}\n"
                    f"Tanlangan to‘garak: {text}"
                ),
            )
        answer = (
            "✅ So‘rovingiz qabul qilindi."
            if admin_chat
            else "So‘rovingiz qayd etildi. "
                 "Administrator hali sozlanmagan."
        )
    elif text == "📢 Yangiliklar":
        answer = (
            "📢 MAKTAB YANGILIKLARI\n\n"
            "Rasmiy yangiliklar shu bo‘limda e'lon qilinadi."
        )
    elif text == "☎️ Bog‘lanish":
        answer = (
            "☎️ BOG‘LANISH\n\n"
            "Maktabning rasmiy aloqa ma'lumotlari "
            "keyinchalik shu yerga kiritiladi."
        )
    else:
        answer = "Iltimos, menyudagi bo‘limlardan birini tanlang."

    await update.message.reply_text(answer)

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN sozlanmagan!")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    app.run_polling()

if __name__ == "__main__":
    main()
  
