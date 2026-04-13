print("BOT STARTING...")
import requests
import os
import telebot
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
def ai_reply(text):
    try:
        key = os.getenv("AI_KEY")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}",
            "Content-Type": "application/json"}
        data = {"model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": text}]}
        r = requests.post(url, json=data, headers=headers, timeout=20)
        return r.json()["choices"][0]["message"]["content"
    except Exception as e:
        return "AI ishlamadi 😔"
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot 24/7 ishlayapti 🚀")
@bot.message_handler(func=lambda message: True)
def handle(message):
    javob = ai_reply(message.text)
    bot.send_message(message.chat.id, javob)
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running')
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()
threading.Thread(target=run_server).start()
bot.infinity_polling(skip_pending=True)
