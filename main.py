import os
import requests
import telebot

# TOKEN
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- AI FUNCTION (SAFE + FREE) ----------------
def ai_reply(text):
    try:
        # Free AI API (agar ishlasa)
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={"message": text},
            timeout=5
        )

        if r.status_code == 200:
            data = r.json()
            if "message" in data:
                return data["message"]

    except:
        pass

    # fallback (har doim ishlaydi)
    return f"🤖 Men sizni tushundim: {text}"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot ishlayapti 🚀")

# ---------------- CHAT ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        reply = ai_reply(message.text)
        bot.send_message(message.chat.id, reply)
    except:
        bot.send_message(message.chat.id, "Xatolik bo‘ldi, lekin bot ishlayapti ✔️")

# ---------------- RUN ----------------
bot.infinity_polling(skip_pending=True)
