import os
import sqlite3
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv(8930013741:AAESISBU0_RrF13ZYtAe4NjhaDlxaCJWkUM)
ADMIN_ID = int(os.getenv("ADMIN_ID", "7746084734"))
DB_NAME = os.getenv("DB_PATH", "maktab.db")

if not TOKEN:
    raise ValueError("BOT_TOKEN maxfiy sozlamasini kiriting!")

bot = telebot.TeleBot(TOKEN)
waiting = {}

CATEGORIES = {
    "school": "🏫 Maktab haqida",
    "schedule": "📅 Dars jadvali",
    "achievements": "🏆 Maktab yutuqlari",
    "clubs": "🎯 To‘garaklar",
    "news": "📢 Yangiliklar",
}


def connect_db():
    con = sqlite3.connect(DB_NAME)
    con.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
    """)
    return con


with connect_db() as con:
    pass


def is_admin(message):
    return (
        message.from_user is not None
        and message.from_user.id == ADMIN_ID
    )


def main_menu(admin=False):
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=2
    )
    kb.add(
        KeyboardButton("🏫 Maktab haqida"),
        KeyboardButton("📅 Jadval"),
        KeyboardButton("🏆 Maktab yutuqlari"),
        KeyboardButton("🎯 To‘garaklar"),
        KeyboardButton("📢 Yangiliklar"),
        KeyboardButton("📞 Bog‘lanish"),
    )
    if admin:
        kb.add(KeyboardButton("🛠 Admin panel"))
    return kb


def admin_menu():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True, row_width=2
    )
    kb.add(
        KeyboardButton("➕ Maktab ma’lumoti"),
        KeyboardButton("➕ Jadval qo‘shish"),
        KeyboardButton("➕ Yutuq qo‘shish"),
        KeyboardButton("➕ To‘garak qo‘shish"),
        KeyboardButton("➕ Yangilik qo‘shish"),
        KeyboardButton("📋 Barcha ma’lumotlar"),
        KeyboardButton("⬅️ Asosiy menyu"),
    )
    return kb


def add_entry(category, title, body):
    with connect_db() as con:
        con.execute(
            "INSERT INTO entries (category, title, body) "
            "VALUES (?, ?, ?)",
            (category, title, body)
        )


def show_category(chat_id, category):
    with connect_db() as con:
        rows = con.execute(
            "SELECT id, title, body FROM entries "
            "WHERE category=? ORDER BY id DESC",
            (category,)
        ).fetchall()

    if not rows:
        bot.send_message(
            chat_id,
            "Bu bo‘limga hali ma’lumot kiritilmagan."
        )
        return

    for item_id, title, body in rows:
        bot.send_message(
            chat_id,
            f"{CATEGORIES[category]}\n\n"
            f"📝 {title}\n\n{body}"
        )


def begin_add(message, category):
    if not is_admin(message):
        bot.send_message(message.chat.id, "⛔ Ruxsat yo‘q.")
        return

    waiting[message.from_user.id] = {
        "category": category
    }
    msg = bot.send_message(
        message.chat.id,
        "📝 Sarlavhani yuboring.\n"
        "Bekor qilish uchun /cancel yozing."
    )
    bot.register_next_step_handler(msg, receive_title)


def receive_title(message):
    uid = message.from_user.id

    if not is_admin(message):
        return

    if message.text == "/cancel":
        waiting.pop(uid, None)
        bot.send_message(message.chat.id, "Bekor qilindi.")
        return

    if not message.text:
        msg = bot.send_message(
            message.chat.id, "Iltimos, matn yuboring."
        )
        bot.register_next_step_handler(msg, receive_title)
        return

    if uid not in waiting:
        bot.send_message(message.chat.id, "Jarayon tugagan.")
        return

    waiting[uid]["title"] = message.text.strip()
    msg = bot.send_message(
        message.chat.id,
        "Endi to‘liq ma’lumotni yuboring:"
    )
    bot.register_next_step_handler(msg, receive_body)


def receive_body(message):
    uid = message.from_user.id

    if not is_admin(message):
        return
        if message.text == "/cancel":
        waiting.pop(uid, None)
        bot.send_message(message.chat.id, "Bekor qilindi.")
        return

    if not message.text:
        msg = bot.send_message(
            message.chat.id, "Ma’lumotni matn qilib yuboring."
        )
        bot.register_next_step_handler(msg, receive_body)
        return

    data = waiting.pop(uid, None)
    if not data:
        bot.send_message(message.chat.id, "Jarayon topilmadi.")
        return

    add_entry(data["category"], data["title"], message.text.strip())
    bot.send_message(
        message.chat.id,
        "✅ Ma’lumot saqlandi!",
        reply_markup=admin_menu()
    )


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! 🏫\n"
        "25-umumiy ta’lim maktabi botiga xush kelibsiz!\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=main_menu(is_admin(message))
    )


@bot.message_handler(commands=["admin"])
def admin_command(message):
    if not is_admin(message):
        bot.reply_to(message, "⛔ Sizda admin huquqi yo‘q.")
        return

    bot.send_message(
        message.chat.id,
        "🛠 25-MAKTAB ADMIN PANELI\n\n"
        "Ma’lumot qo‘shish, tahrirlash yoki o‘chirish "
        "uchun quyidagi tugmalardan foydalaning.\n"
        "Buyruqlar: /all, /edit ID, /delete ID",
        reply_markup=admin_menu()
    )


@bot.message_handler(commands=["cancel"])
def cancel(message):
    waiting.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, "Jarayon bekor qilindi.")


@bot.message_handler(commands=["all"])
def all_entries(message):
    if not is_admin(message):
        bot.reply_to(message, "⛔ Ruxsat yo‘q.")
        return

    with connect_db() as con:
        rows = con.execute(
            "SELECT id, category, title FROM entries ORDER BY id DESC"
        ).fetchall()

    if not rows:
        bot.send_message(message.chat.id, "Ma’lumotlar hali yo‘q.")
        return

    for item_id, category, title in rows:
        bot.send_message(
            message.chat.id,
            f"ID: {item_id}\n"
            f"Bo‘lim: {CATEGORIES[category]}\n"
            f"Sarlavha: {title}\n\n"
            f"Tahrirlash: /edit {item_id}\n"
            f"O‘chirish: /delete {item_id}"
        )


@bot.message_handler(commands=["edit"])
def edit_entry(message):
    if not is_admin(message):
        bot.reply_to(message, "⛔ Ruxsat yo‘q.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Foydalanish: /edit ID")
        return

    item_id = int(parts[1])

    with connect_db() as con:
        row = con.execute(
            "SELECT title, body FROM entries WHERE id=?",
            (item_id,)
        ).fetchone()

    if not row:
        bot.reply_to(message, "ID topilmadi.")
        return

    waiting[message.from_user.id] = {
        "action": "edit_title",
        "id": item_id
    }
    msg = bot.send_message(
        message.chat.id,
        f"Eski sarlavha: {row[0]}\nYangi sarlavhani yuboring:"
    )
    bot.register_next_step_handler(msg, edit_title_step)


def edit_title_step(message):
    if not is_admin(message):
        return

    if message.text == "/cancel":
        waiting.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "Bekor qilindi.")
        return

    data = waiting.get(message.from_user.id)
    if not data:
        return

    data["new_title"] = message.text.strip()
    msg = bot.send_message(
        message.chat.id, "Yangi to‘liq ma’lumotni yuboring:"
    )
    bot.register_next_step_handler(msg, edit_body_step)


def edit_body_step(message):
    if not is_admin(message):
        return

    if message.text == "/cancel":
        waiting.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "Bekor qilindi.")
        return
        data = waiting.pop(message.from_user.id, None)
    if not data or not message.text:
        bot.send_message(message.chat.id, "Tahrirlash bekor qilindi.")
        return

    with connect_db() as con:
        cur = con.execute(
            "UPDATE entries SET title=?, body=? WHERE id=?",
            (data["new_title"], message.text.strip(), data["id"])
        )

    bot.send_message(
        message.chat.id,
        "✅ Yangilandi." if cur.rowcount else "ID topilmadi."
    )


@bot.message_handler(commands=["delete"])
def delete_entry(message):
    if not is_admin(message):
        bot.reply_to(message, "⛔ Ruxsat yo‘q.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Foydalanish: /delete ID")
        return

    with connect_db() as con:
        cur = con.execute(
            "DELETE FROM entries WHERE id=?",
            (int(parts[1]),)
        )

    bot.reply_to(
        message,
        "✅ O‘chirildi." if cur.rowcount else "ID topilmadi."
    )


@bot.message_handler(func=lambda m: m.text == "🛠 Admin panel")
def admin_button(message):
    if is_admin(message):
        bot.send_message(
            message.chat.id,
            "🛠 Admin panel",
            reply_markup=admin_menu()
        )
    else:
        bot.reply_to(message, "⛔ Ruxsat yo‘q.")


@bot.message_handler(func=lambda m: m.text == "➕ Maktab ma’lumoti")
def add_school(message):
    begin_add(message, "school")


@bot.message_handler(func=lambda m: m.text == "➕ Jadval qo‘shish")
def add_schedule(message):
    begin_add(message, "schedule")


@bot.message_handler(func=lambda m: m.text == "➕ Yutuq qo‘shish")
def add_achievement(message):
    begin_add(message, "achievements")


@bot.message_handler(func=lambda m: m.text == "➕ To‘garak qo‘shish")
def add_club(message):
    begin_add(message, "clubs")


@bot.message_handler(func=lambda m: m.text == "➕ Yangilik qo‘shish")
def add_news(message):
    begin_add(message, "news")


@bot.message_handler(func=lambda m: m.text == "📋 Barcha ma’lumotlar")
def list_button(message):
    if is_admin(message):
        all_entries(message)


@bot.message_handler(func=lambda m: m.text == "⬅️ Asosiy menyu")
def back(message):
    bot.send_message(
        message.chat.id,
        "Asosiy menyu:",
        reply_markup=main_menu(is_admin(message))
    )


@bot.message_handler(func=lambda m: m.text == "📅 Jadval")
def schedule(message):
    show_category(message.chat.id, "schedule")


@bot.message_handler(func=lambda m: m.text == "🏫 Maktab haqida")
def school(message):
    show_category(message.chat.id, "school")


@bot.message_handler(func=lambda m: m.text == "🏆 Maktab yutuqlari")
def achievements(message):
    show_category(message.chat.id, "achievements")


@bot.message_handler(func=lambda m: m.text == "🎯 To‘garaklar")
def clubs(message):
    show_category(message.chat.id, "clubs")


@bot.message_handler(func=lambda m: m.text == "📢 Yangiliklar")
def news(message):
    show_category(message.chat.id, "news")


@bot.message_handler(func=lambda m: m.text == "📞 Bog‘lanish")
def contact(message):
    show_category(message.chat.id, "school")


@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(
        message.chat.id,
        "Kerakli bo‘limni pastdagi menyudan tanlang.",
        reply_markup=main_menu(is_admin(message))
    )


print("25-maktab boti ishga tushdi!")
bot.infinity_polling(skip_pending=True)
