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

# ---------------- AI (STABLE FALLBACK SYSTEM) ----------------
def ai_reply(text):
    # 1-TRY (primary free API)
    try:
        url = "https://api.affiliateplus.xyz/api/chatbot"
        r = requests.get(url, params={
            "message": text,
            "botname": "AI",
            "ownername": "user"
        }, timeout=10)

        if r.status_code == 200:
            data = r.json()
            if "message" in data:
                return data["message"]
    except:
        pass

    # 2-TRY (backup simple response)
    try:
        return "🤖 Men hozir AI serverga ulanolmadim, lekin savolingizni oldim: " + text
    except:
        return "AI hozir ishlamayapti 😔"

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
