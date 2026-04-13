import os
import requests
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

def ai_reply(text):
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={"message": text},
            timeout=10
        )
        if r.status_code == 200:
            return r.json().get("message", "AI javob yo‘q")
    except:
        pass

    return "AI hozir ishlamayapti 😔"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot ishlayapti ✔️")

# ⭐ ENG MUHIM QISM
@bot.message_handler(func=lambda message: True)
def handle(message):
    reply = ai_reply(message.text)
    bot.send_message(message.chat.id, reply)

bot.infinity_polling(skip_pending=True)
