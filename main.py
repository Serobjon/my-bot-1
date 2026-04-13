import os
import requests
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- MATH CHECK ----------------
def is_math(text):
    ops = ["+", "-", "*", "/", "(", ")", "^"]
    return any(op in text for op in ops)

def calc_math(text):
    try:
        text = text.replace("^", "**")
        return eval(text)
    except:
        return "Hisoblab bo‘lmadi ❌"

# ---------------- AI ----------------
def ai_reply(text):

    # 1️⃣ MATH PRIORITY
    if is_math(text):
        return f"🧮 Javob: {calc_math(text)}"

    # 2️⃣ FREE AI
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={"message": text},
            timeout=5
        )
        if r.status_code == 200:
            return r.json().get("message", "")
    except:
        pass

    # 3️⃣ FALLBACK
    return f"🤖 Men sizni tushundim: {text}"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot ishlayapti 🚀\nMatematikani ham yechaman 🧮")

# ---------------- ALL MESSAGES ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        bot.send_message(message.chat.id, ai_reply(message.text))
    except:
        bot.send_message(message.chat.id, "Xatolik bo‘ldi ❌")

bot.infinity_polling(skip_pending=True)
