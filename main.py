import os
import telebot
from sympy import symbols, Eq, solve, sympify

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

x = symbols('x')

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🧮 Math Bot\n\n"
        "Misollar:\n"
        "x+5=10\n"
        "x^2+5*x+6=0\n"
        "2+2"
    )

# ---------------- SOLVER ----------------
def solve_all(text):
    try:
        text = text.replace("^", "**")

        # 1️⃣ EQUATION (oddiy + kvadrat ham)
        if "=" in text:
            left, right = text.split("=")
            eq = Eq(sympify(left), sympify(right))
            sol = solve(eq, x)
            return f"🧠 x = {sol}"

        # 2️⃣ NORMAL MATH
        return f"🧮 {sympify(text)}"

    except:
        return "❌ Xato misol"

# ---------------- HANDLE ----------------
@bot.message_handler(func=lambda m: True)
def handle(message):
    result = solve_all(message.text)
    bot.send_message(message.chat.id, result)

bot.infinity_polling(skip_pending=True)
