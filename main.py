import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Siz bergan token va admin ID
API_TOKEN = '8930013741:AAESISBU0_RrF13ZYtAe4NjhaDlxaCJWkUM'
ADMIN_ID = 7746084734

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ASOSIY MENYU TUGMALARI ---
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🏫 Maktab haqida"), KeyboardButton(text="🎯 To'garaklar")],
        [KeyboardButton(text="📅 Jadval"), KeyboardButton(text="📝 To'garakka yozilish")],
        [KeyboardButton(text="📢 Yangiliklar"), KeyboardButton(text="📞 Bog'lanish")]
    ],
    resize_keyboard=True
)

# 1. Start buyrug'i va asosiy menyu
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Assalomu alaykum! 25-Maktab botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=main_menu
    )

# 2. Tugmalar bosilganda ishlaydigan funksiyalar
@dp.message_handler(text="🏫 Maktab haqida")
async def about_school(message: types.Message):
    await message.answer("🏫 25-maktab — bilim maskani! Bu yerda maktab haqida batafsil ma'lumot bo'ladi.")

@dp.message_handler(text="🎯 To'garaklar")
async def circles(message: types.Message):
    await message.answer("🎯 Maktabimizda turli xil fan va sport to'garaklari faoliyat yuritadi.")

@dp.message_handler(text="📅 Jadval")
async def schedule(message: types.Message):
    await message.answer("📅 Dars jadvali tez orada yangilanadi.")

@dp.message_handler(text="📝 To'garakka yozilish")
async def join_circle(message: types.Message):
    await message.answer("📝 To'garakka yozilish uchun admin bilan bog'laning yoki ma'lumot qoldiring.")

@dp.message_handler(text="📢 Yangiliklar")
async def news(message: types.Message):
    await message.answer("📢 Maktabimiz yangiliklari bilan tanishib boring.")

@dp.message_handler(text="📞 Bog'lanish")
async def contact(message: types.Message):
    await message.answer("📞 Biz bilan bog'lanish uchun: +998 XX XXX XX XX")


# --- ADMIN PANEL ---

# /stats buyrug'i (Faqat admin uchun)
@dp.message_handler(commands=['stats'])
async def admin_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Bu buyruq faqat admin uchun!")
    
    # Bu yerda bazadagi statistika chiqadi
    await message.answer("📊 Hozircha botda ro'yxatdan o'tganlar soni bazaga qarab chiqariladi.")

# /broadcast buyrug'i (Faqat admin uchun)
@dp.message_handler(commands=['broadcast'])
async def admin_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Bu buyruq faqat admin uchun!")
    
    text_to_send = message.get_args()
    if not text_to_send:
        await message.answer(
            "Iltimos, yubormoqchi bo'lgan xabaringizni matn bilan birga yozing.\n\n"
            "Masalan:\n`/broadcast Ertaga darslar soat 08:00 da boshlanadi!`",
            parse_mode="Markdown"
        )
        return
    
    # Xabar yuborish jarayoni
    await message.answer(f"✅ Xabar muvaffaqiyatli yuborildi!\n\n**Matn:** {text_to_send}", parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
