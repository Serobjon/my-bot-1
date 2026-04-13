import os
import telebot
import requests

# ---------------- SAFE TOKEN LOAD ----------------
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ TOKEN topilmadi!")
    TOKEN = "0"

bot = telebot.TeleBot(TOKEN)

# ---------------- SAFE AI ----------------
def ai_reply(text):

    # 🔵 1-URINISH (FREE API)
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={"message": text},
            timeout=5
        )

        if r.status_code == 200:
            data = r.json()
            return data.get("message", "AI javob yo‘q")

    except Exception as e:
        print("AI error:", e)

    # 🟡 2-FALLBACK
    try:
        return f"🤖 Men sizni tushundim: {text}"
    except:
        pass

    # 🔴 FINAL SAFETY
    return "🤖 Hozir tizim javob bera olmadi"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, "Bot ishlayapti 🚀")
    except Exception as e:
        print("Start error:", e)

# ---------------- ALL MESSAGES ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        reply = ai_reply(message.text)
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        print("Handler error:", e)

# ---------------- RUN SAFE ----------------
print("Bot ishga tushdi ✔️")

while True:
    try:
        bot.infinity_polling(skip_pending=True, timeout=10, long_polling_timeout=10)
    except Exception as e:
        print("Restarting bot due to error:", e)
