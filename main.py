import os
import telebot
from sympy import symbols, Eq, solve, simplify

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
        "x^2+5*x+6=0"
    )

# ---------------- SOLVER ----------------
def solve_text(text):
    try:
        text = text.replace("^", "**")

        # 1️⃣ TENGLAMA (kvadrat ham)
        if "=" in text:
            left, right = text.split("=")

            eq = Eq(simplify(left), simplify(right))
            sol = solve(eq, x)

            return f"🧠 x = {sol}"

        # 2️⃣ NORMAL MATH
        return f"🧮 {simplify(text)}"

    except:
        return "❌ Xato misol"

# ---------------- HANDLE ----------------
@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_message(m.chat.id, solve_text(m.text))

bot.infinity_polling(skip_pending=True)
