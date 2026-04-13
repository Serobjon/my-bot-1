import os
import telebot
import requests
import base64
from sympy import symbols, Eq, solve, simplify

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

x = symbols('x')

# ---------------- MATH ENGINE ----------------
def solve_math(text):
    try:
        text = text.replace("^", "**")

        if "=" in text:
            left, right = text.split("=")

            eq = Eq(simplify(left), simplify(right))
            sol = solve(eq, x)

            return f"🧠 x = {sol}"

        # oddiy expression
        return f"🧮 {simplify(text)}"

    except:
        return None

# ---------------- AI CHAT (FREE) ----------------
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
            b64 = base64.b64encode(f.read()).decode()

        r = requests.post(
            "https://api.deepai.org/api/vision",
            data={"image": "data:image/jpeg;base64," + b64},
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
    bot.send_message(
        m.chat.id,
        "🚀 MAX AI BOT\n\n"
        "🧠 Algebra\n🧮 Math\n🤖 AI\n🖼 Image"
    )

# ---------------- PHOTO ----------------
@bot.message_handler(content_types=['photo'])
def photo(m):
    file_info = bot.get_file(m.photo[-1].file_id)
    downloaded = bot.download_file(file_info.file_path)

    path = "img.jpg"
    with open(path, "wb") as f:
        f.write(downloaded)

    res = image_ai(path)
    bot.send_message(m.chat.id, "🖼 " + res)

# ---------------- TEXT ----------------
@bot.message_handler(func=lambda m: True)
def handle(m):

    text = m.text

    # 1️⃣ math/algebra first
    math = solve_math(text)
    if math:
        bot.send_message(m.chat.id, math)
        return

    # 2️⃣ AI second
    bot.send_message(m.chat.id, ai(text))

bot.infinity_polling(skip_pending=True)
