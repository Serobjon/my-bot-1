import os
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- SAFE MATH ----------------
def calc(text):
    try:
        text = text.replace("^", "**")
        return eval(text)
    except:
        return "Hisoblab bo‘lmadi ❌"

def is_math(text):
    symbols = ["+", "-", "*", "/", "^", "(", ")"]
    return any(s in text for s in symbols)

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🧮 Math bot ishga tushdi!\nMasalan: 2+2 yozing")

# ---------------- MATH HANDLER ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text

    if is_math(text):
        result = calc(text)
        bot.send_message(message.chat.id, f"🧮 Javob: {result}")
    else:
        bot.send_message(message.chat.id, "Faqat matematika yozing 🧮")

# ---------------- RUN ----------------
bot.infinity_polling(skip_pending=True)
