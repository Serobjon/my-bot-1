import os
import telebot
import requests
from sympy import symbols, Eq, solve
from PIL import Image
import io
import base64

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

x = symbols('x')

# ---------------- MATH (Qiyin tenglama) ----------------
def solve_math(text):
    try:
        text = text.replace("^", "**")

        if "=" in text:
            left, right = text.split("=")
            eq = Eq(eval(left), eval(right))
            sol = solve(eq, x)
            return f"🧠 x = {sol}"

    except:
        return None

# ---------------- AI ----------------
def ai(text):
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={"message": text},
            timeout=6
        )
        if r.status_code == 200:
            return r.json().get("message", "")
    except:
        pass

    return "🤖 Hozir AI javob bera olmadi"

# ---------------- IMAGE ANALYSIS ----------------
def image_ai(file_path):
    try:
        with open(file_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()

        r = requests.post(
            "https://api.deepai.org/api/vision",
            data={"image": "data:image/jpeg;base64," + img_b64},
            timeout=10
        )

        if r.status_code == 200:
            return r.json().get("output", "🖼 Tahlil qilindi")
    except:
        pass

    return "🖼 Rasmni tahlil qilib bo‘lmadi"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
        "🚀 MAX AI BOT\n\n"
        "🧠 Math\n🤖 AI\n🖼 Image"
    )

# ---------------- PHOTO ----------------
@bot.message_handler(content_types=['photo'])
def photo(m):
    file_info = bot.get_file(m.photo[-1].file_id)
    downloaded = bot.download_file(file_info.file_path)

    path = "img.jpg"
    with open(path, "wb") as f:
        f.write(downloaded)

    result = image_ai(path)
    bot.send_message(m.chat.id, "🖼 " + result)

# ---------------- TEXT ----------------
@bot.message_handler(func=lambda m: True)
def handle(m):

    text = m.text

    # math first
    math = solve_math(text)
    if math:
        bot.send_message(m.chat.id, math)
        return

    # AI second
    bot.send_message(m.chat.id, ai(text))

bot.infinity_polling(skip_pending=True)
