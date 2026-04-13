import os
import telebot
import requests
import re
import base64

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- MATH ----------------
def calc(text):
    try:
        text = text.replace("^", "**")
        allowed = "0123456789+-*/(). x="
        if not all(c in allowed for c in text):
            return None
        return eval(text)
    except:
        return None

# ---------------- EQUATION ----------------
def solve_eq(text):
    try:
        if "=" not in text:
            return None

        left, right = text.split("=")
        right = float(eval(right.strip()))

        match = re.match(r"([0-9]*)x\s*([\+\-]?\s*\d+)?", left.strip())
        if match:
            a = match.group(1)
            b = match.group(2)

            a = float(a) if a not in ["", None] else 1
            b = float(b.replace(" ", "")) if b else 0

            x = (right - b) / a
            return f"x = {x}"
    except:
        return None

# ---------------- FREE AI ----------------
def ai(text):
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

    return "🤖 Men sizni tushundim, lekin AI hozir band."

# ---------------- IMAGE ANALYSIS ----------------
def analyze_image(file_path):
    try:
        with open(file_path, "rb") as img:
            b64 = base64.b64encode(img.read()).decode()

        # FREE demo vision API (not perfect but works)
        r = requests.post(
            "https://api.deepai.org/api/vision",
            data={"image": "data:image/jpeg;base64," + b64},
            timeout=10
        )

        if r.status_code == 200:
            return r.json().get("output", "Rasm tahlil qilindi")
    except:
        pass

    return "🖼 Rasmni tahlil qilib bo‘lmadi"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(
        m.chat.id,
        "🚀 MAX BOT ishga tushdi!\n\n🧮 Math\n🧠 AI\n🖼 Image"
    )

# ---------------- PHOTO ----------------
@bot.message_handler(content_types=['photo'])
def photo(m):
    file_info = bot.get_file(m.photo[-1].file_id)
    downloaded = bot.download_file(file_info.file_path)

    path = "img.jpg"
    with open(path, "wb") as f:
        f.write(downloaded)

    result = analyze_image(path)
    bot.send_message(m.chat.id, "🖼 " + result)

# ---------------- TEXT ----------------
@bot.message_handler(func=lambda m: True)
def handle(m):

    text = m.text

    eq = solve_eq(text)
    if eq:
        bot.send_message(m.chat.id, "🧠 " + eq)
        return

    math = calc(text)
    if math is not None:
        bot.send_message(m.chat.id, "🧮 " + str(math))
        return

    bot.send_message(m.chat.id, ai(text))

bot.infinity_polling(skip_pending=True)
