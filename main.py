import os
import telebot
import requests
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- WEB SERVER (KEEP ALIVE) ----------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---------------- SAFE MATH ----------------
def calc(text):
    try:
        text = text.replace("^", "**")
        allowed = "0123456789+-*/(). "
        for ch in text:
            if ch not in allowed:
                return None
        return str(eval(text))
    except:
        return None

# ---------------- AI ----------------
def ai_reply(text):

    # MATH
    result = calc(text)
    if result:
        return f"🧮 Javob: {result}"

    # FREE AI
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

    # FALLBACK
    return f"🤖 Menimcha siz: {text}"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 AI + Math bot ishlayapti!")

# ---------------- CHAT ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        bot.send_message(message.chat.id, ai_reply(message.text))
    except:
        bot.send_message(message.chat.id, "Xatolik 😔")

# ---------------- RUN ----------------
keep_alive()

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("Restart:", e)
