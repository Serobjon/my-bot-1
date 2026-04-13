import requests

def ai_reply(text):

    # 1️⃣ AI API (free, lekin ba'zan ishlamasligi mumkin)
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={"message": text},
            timeout=6
        )
        if r.status_code == 200:
            data = r.json()
            if "message" in data:
                return data["message"]
    except:
        pass

    # 2️⃣ SMART FALLBACK (har doim ishlaydi)
    try:
        return f"🤖 Men sizni tushundim: {text}"
    except:
        return "🤖 Hozir javob bera olmadim"
