import os
import telebot

TOKEN = os.getenv("TOKEN")

print("TOKEN =", TOKEN)

if not TOKEN:
    print("TOKEN YO‘Q ❌")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "START ISHLAYAPTI ✔️")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.send_message(message.chat.id, "OK: " + message.text)

bot.infinity_polling(skip_pending=True)
