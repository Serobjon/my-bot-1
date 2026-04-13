import os
import requests
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- AI SYSTEM (STABLE FREE) ----------------
def ai_reply(text):

    # 1️⃣ API 1
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={"message": text},
            timeout=6
        )
        if r.status_code == 200:
            data = r.json()
            if "message" in data:
                return data["message"]
    except:
        pass

    # 2️⃣ API 2 (backup)
    try:
        r = requests.get("https://api.quotable.io/random", timeout=5)
        if r.status_code == 200:
            q = r.json()
            return f"🤖 {q['content']}"
    except:
        pass

    # 3️⃣ ALWAYS WORKS
    return f"🤖 Savolingiz qabul qilindi: {text}"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot ishlayapti 🚀")

# ---------------- CHAT ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    bot.send_message(message.chat.id, ai_reply(message.text))

bot.infinity_polling(skip_pending=True)
