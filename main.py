import os
import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# TOKEN
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- MENU ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🤖 AI"), KeyboardButton("ℹ️ Help"))
    return markup

# --- AI FUNCTION ---
def ai_reply(text):
    try:
        key = os.getenv("AI_KEY")

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]
        }

        r = requests.post(url, json=data, headers=headers, timeout=20)
        return r.json()["choices"][0]["message"]["content"]

    except:
        return "AI ishlamadi 😔"

# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Bot ishlayapti 🚀\nQuyidan tanlang 👇",
        reply_markup=main_menu()
    )

# --- MENU BUTTONS ---
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_msg(message):
    bot.send_message(message.chat.id, "Savol yozing yoki AI tugmasini bosing 🤖")

@bot.message_handler(func=lambda m: m.text == "🤖 AI")
def ai_info(message):
    bot.send_message(message.chat.id, "Savol yozing, men javob beraman 🤖")

# --- AI CHAT ---
@bot.message_handler(func=lambda message: True)
def handle(message):
    javob = ai_reply(message.text)
    bot.send_message(message.chat.id, javob)

# --- RUN BOT ---
bot.infinity_polling(skip_pending=True)
