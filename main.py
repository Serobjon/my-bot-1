import requests
import os
import telebot

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

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

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot ishlayapti 🤖")

@bot.message_handler(func=lambda message: True)
def handle(message):
    javob = ai_reply(message.text)
    bot.send_message(message.chat.id, javob)

bot.infinity_polling(skip_pending=True)
