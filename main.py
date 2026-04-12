import requests
import os

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
import os
import telebot

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot 24/7 ishlayapti 🚀")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling(skip_pending=True)
