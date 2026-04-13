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
        "🧮 Math Bot ishga tushdi!\n\n"
        "Misollar:\n"
        "2+2\n"
        "x+5=10\n"
        "x^2+5*x+6=0\n"
        "x*(5+6)-x*(3+2)=20"
    )

# ---------------- MATH ENGINE ----------------
def solve_math(text):
    try:
        text = text.replace("^", "**")

        # 1️⃣ EQUATION (oddiy + kvadrat + murakkab)
        if "=" in text:
            left, right = text.split("=")
            eq = Eq(sympify(left), sympify(right))
            sol = solve(eq, x)
            return f"🧠 x = {sol}"

        # 2️⃣ NORMAL MATH
        return f"🧮 {sympify(text)}"

    except:
        return "❌ Noto‘g‘ri misol"

# ---------------- HANDLE ----------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    result = solve_math(message.text)
    bot.send_message(message.chat.id, result)

bot.infinity_polling(skip_pending=True)
