import os
import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ.get("TOKEN")
AI_KEY = os.environ.get("AI_KEY")

bot = telebot.TeleBot(TOKEN)

# ---------------- MENU ----------------
def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🤖 AI"), KeyboardButton("ℹ️ Help"))
    return kb

# ---------------- AI ----------------
def ai_reply(text):
    try:
        if not AI_KEY:
            return "AI_KEY yo‘q 😔"

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {AI_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]
        }

        r = requests.post(url, json=data, headers=headers, timeout=15)

        if r.status_code != 200:
            return f"AI error 😔 ({r.status_code})"

        return r.json()["choices"][0]["message"]["content"]

    except Exception:
        return "AI ishlamadi 😔"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Bot ishlayapti 🚀",
        reply_markup=menu()
    )

# ---------------- MENU BUTTONS ----------------
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_cmd(message):
    bot.send_message(message.chat.id, "Savol yozing yoki AI tugmasini bosing 🤖")

@bot.message_handler(func=lambda m: m.text == "🤖 AI")
def ai_btn(message):
    bot.send_message(message.chat.id, "Savol yozing 🤖")

# ---------------- CHAT ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    bot.send_message(message.chat.id, ai_reply(message.text))

# ---------------- RUN ----------------
bot.infinity_polling(skip_pending=True)
