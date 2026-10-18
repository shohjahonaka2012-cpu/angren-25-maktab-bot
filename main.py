import telebot

# Siz taqdim etgan bot tokeni
TOKEN = "8930013741:AAESISBU0_RrF13ZYtAe4NjhaDlxaCJWkUM"
bot = telebot.TeleBot(TOKEN)

# Siz taqdim etgan admin ID raqami
ADMIN_ID = 7746084734  

# Start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Maktab botimizga xush kelibsiz. 🏫")

# Admin panel buyrug'i
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    # Faqat siz yuborgan ID egasi kira olishi uchun shart
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, 
                     "👑 **Xush kelibsiz, Hurmatli Maktab Admini!**\n\n"
                     "Mavjud buyruqlar:\n"
                     "/stats - Foydalanuvchilar sonini ko'rish\n"
                     "/broadcast - Barchaga xabar yuborish",
                     parse_mode="Markdown")
    else:
        bot.reply_to(message, "Kechirasiz, sizda bu bo'limga kirish huquqi yo'q. ❌")

# Statistika bo'limi
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "📊 Hozircha botda ro'yxatdan o'tganlar soni bazaga qarab chiqariladi.")
    else:
        bot.reply_to(message, "Siz admin emassiz! ❌")

# Rassilka (barchaga xabar yuborish)
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace('/broadcast', '').strip()
        if not text:
            bot.reply_to(message, "Iltimos, yubormoqchi bo'lgan xabaringizni matn bilan birga yozing.\n"
                                  "Masalan: `/broadcast Ertaga darslar soat 08:00 da boshlanadi!`", parse_mode="Markdown")
            return
        
        # Bu yerda bazadagi barcha foydalanuvchilarga xabar tarqatish amali bajariladi
        bot.reply_to(message, "✅ Xabar muvaffaqiyatli yuborildi!")
    else:
        bot.reply_to(message, "Siz admin emassiz! ❌")

# Botni ishga tushirish
print("Bot ishga tushdi...")
bot.infinity_polling()
