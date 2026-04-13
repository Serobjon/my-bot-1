import os
import telebot
import re

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# ---------------- BASIC MATH ----------------
def safe_eval(expr):
    try:
        expr = expr.replace("^", "**")
        allowed = "0123456789+-*/(). x="
        if not all(c in allowed for c in expr):
            return None
        return eval(expr)
    except:
        return None

# ---------------- EQUATION SOLVER ----------------
def solve_equation(text):
    try:
        # example: x + 5 = 10
        if "=" not in text:
            return None

        left, right = text.split("=")
        left = left.strip()
        right = float(eval(right))

        # simple form: ax + b
        match = re.match(r"([0-9]*)x\s*([\+\-]?\s*\d+)?", left)

        if match:
            a = match.group(1)
            b = match.group(2)

            a = float(a) if a not in ["", None] else 1
            b = float(b.replace(" ", "")) if b else 0

            x = (right - b) / a
            return f"x = {x}"

    except:
        return None

# ---------------- AI / LOGIC ----------------
def reply(text):

    # 1️⃣ equation
    eq = solve_equation(text)
    if eq:
        return "🧠 " + eq

    # 2️⃣ normal math
    math = safe_eval(text)
    if math is not None:
        return "🧮 " + str(math)

    # 3️⃣ fallback
    return "🤖 Men faqat matematikani yecha olaman. Misol: 2+2 yoki x+5=10"

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
        "🤖 Math Bot ishga tushdi!\n\n"
        "🧮 Misollar: 2+2, 10/2\n"
        "🧠 Tenglama: x+5=10"
    )

# ---------------- HANDLE ----------------
@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_message(m.chat.id, reply(m.text))

bot.infinity_polling(skip_pending=True)
