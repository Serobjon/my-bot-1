import requests

def ai_reply(text):

    # 1️⃣ API 1 (chatbot free)
    try:
        r = requests.get(
            "https://api.affiliateplus.xyz/api/chatbot",
            params={
                "message": text,
                "botname": "AI",
                "ownername": "user"
            },
            timeout=6
        )
        if r.status_code == 200:
            data = r.json()
            if "message" in data:
                return data["message"]
    except:
        pass

    # 2️⃣ API 2 (public QA)
    try:
        r = requests.get("https://api.quotable.io/random", timeout=5)
        if r.status_code == 200:
            q = r.json()
            return f"🤖 AI band, lekin mana javob:\n\n{q['content']}"
    except:
        pass

    # 3️⃣ API 3 (fallback har doim ishlaydi)
    return f"🤖 Savolingiz: {text}\n\nHozir AI serverlar band, keyin qayta urinib ko‘ring 🙂"
