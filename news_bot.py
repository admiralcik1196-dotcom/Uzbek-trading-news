import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

now = datetime.now(ZoneInfo("Asia/Tashkent"))
message = (
    "🤖 AI TRADING NEWS\n\n"
    f"📅 Sana: {now:%d.%m.%Y}\n"
    f"🕒 Vaqt: {now:%H:%M} (O‘zbekiston)\n\n"
    "🇺🇸 USD va 🥇 XAUUSD yangiliklari botimiz sozlanmoqda!\n"
    "Keyingi bosqichda iqtisodiy kalendar va bozor tahlili ulanadi."
)

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
response = requests.post(
    url,
    json={"chat_id": CHAT_ID, "text": message},
    timeout=20
)
response.raise_for_status()
print("Telegram xabari yuborildi!")
print(response.tex
