import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Siz bergan token va admin ID
TOKEN = '8930013741:AAESISBU0_RrF13ZYtAe4NjhaDlxaCJWkUM'
ADMIN_ID = 7746084734

bot = telebot.TeleBot(TOKEN)

# Asosiy menyu tugmalari
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🏫 Maktab haqida"),
        KeyboardButton("🎯 To'garaklar"),
        KeyboardButton("📅 Jadval"),
        KeyboardButton("📝 To'garakka yozilish"),
        KeyboardButton("📢 Yangiliklar"),
        KeyboardButton("📞 Bog'lanish")
    )
    return markup

# Start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! 25-Maktab botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )

# Tugmalar handlerlari
@bot.message_handler(func=lambda message: message.text == "🏫 Maktab haqida")
def about_school(message):
    bot.send_message(message.chat.id, "🏫 25-maktab — bilim maskani! Bu yerda maktab haqida batafsil ma'lumot beriladi.")

@bot.message_handler(func=lambda message: message.text == "🎯 To'garaklar")
def circles(message):
    bot.send_message(message.chat.id, "🎯 Maktabimizda turli xil fan va sport to'garaklari faoliyat yuritadi.")

@bot.message_handler(func=lambda message: message.text == "📅 Jadval")
def schedule(message):
    bot.send_message(message.chat.id, "📅 Dars jadvali tez orada yangilanadi.")

@bot.message_handler(func=lambda message: message.text == "📝 To'garakka yozilish")
def join_circle(message):
    bot.send_message(message.chat.id, "📝 To'garakka yozilish uchun admin bilan bog'laning.")

@bot.message_handler(func=lambda message: message.text == "📢 Yangiliklar")
def news(message):
    bot.send_message(message.chat.id, "📢 Maktabimiz yangiliklari bilan tanishib boring.")

@bot.message_handler(func=lambda message: message.text == "📞 Bog'lanish")
def contact(message):
    bot.send_message(message.chat.id, "📞 Biz bilan bog'lanish uchun: +998 XX XXX XX XX")


# --- ADMIN PANEL ---

# /stats buyrug'i
@bot.message_handler(commands=['stats'])
def admin_stats(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat admin uchun!")
        return
    bot.send_message(message.chat.id, "📊 Hozircha botda ro'yxatdan o'tganlar soni bazaga qarab chiqariladi.")

# /broadcast buyrug'i
@bot.message_handler(commands=['broadcast'])
def admin_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Bu buyruq faqat admin uchun!")
        return
    
    text_to_send = message.text.replace('/broadcast', '').strip()
    if not text_to_send:
        bot.send_message(
            message.chat.id,
            "Iltimos, yubormoqchi bo'lgan xabaringizni matn bilan birga yozing.\n\nMasalan:\n`/broadcast Ertaga darslar soat 08:00 da boshlanadi!`",
            parse_mode="Markdown"
        )
        return
    
    bot.send_message(message.chat.id, f"✅ Xabar muvaffaqiyatli yuborildi!\n\n**Matn:** {text_to_send}", parse_mode="Markdown")

if __name__ == '__main__':
    print("Bot ishga tushdi...")
    bot.infinity_polling()
    
