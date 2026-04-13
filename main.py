import os
import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- MENU ----------------
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🤖 AI"), KeyboardButton("ℹ️ Help"))
    return kb

# ---------------- AI SYSTEM (3 LEVEL) ----------------
def ai_reply(text):

    # 🔵 LEVEL 1 (Primary free API)
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={
                "message": text,
                "botname": "AI",
                "ownername": "user"
            },
            timeout=8
        )
        if r.status_code == 200:
            data = r.json()
            if "message" in data:
                return data["message"]
    except:
        pass

    # 🟡 LEVEL 2 (simple fallback API)
    try:
        r = requests.get(
            "https://api.quotable.io/random",
            timeout=5
        )
        if r.status_code == 200:
            quote = r.json()
            return f"🤖 AI hozir band, lekin mana javob:\n\n{quote['content']}"
    except:
        pass

    # 🔴 LEVEL 3 (offline fallback - always works)
    return f"🤖 Savolingiz qabul qilindi: {text}\n\nHozir AI serverlar band 😔"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot ishlayapti 🚀", reply_markup=menu())

# ---------------- HELP ----------------
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_cmd(message):
    bot.send_message(message.chat.id, "Savol yozing 🤖")

# ---------------- AI BUTTON ----------------
@bot.message_handler(func=lambda m: m.text == "🤖 AI")
def ai_btn(message):
    bot.send_message(message.chat.id, "Savol yozing 🤖")

# ---------------- CHAT ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    bot.send_message(message.chat.id, ai_reply(message.text))

bot.infinity_polling(skip_pending=True)
