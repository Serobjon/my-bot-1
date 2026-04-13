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

# ---------------- FREE AI (NO CREDIT) ----------------
def ai_reply(text):
    try:
        # FREE PUBLIC AI (no key needed)
        url = "https://api.affiliateplus.xyz/api/chatbot"

        params = {
            "message": text,
            "botname": "AI",
            "ownername": "user"
        }

        r = requests.get(url, params=params, timeout=15)

        if r.status_code != 200:
            return "AI hozir ishlamayapti 😔"

        return r.json().get("message", "AI javob yo‘q")

    except:
        return "AI error 😔 lekin bot ishlayapti ✔️"

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
