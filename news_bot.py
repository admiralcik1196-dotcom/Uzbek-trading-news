import os
import requests
from datetime import datetime, date
from zoneinfo import ZoneInfo

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
UZ = ZoneInfo("Asia/Tashkent")
NY = ZoneInfo("America/New_York")

now = datetime.now(UZ)
today = now.date()

message = [
    "🤖 AI TRADING NEWS",
    "",
    f"📅 Sana: {now:%d.%m.%Y}",
    "🕒 Vaqt: O‘zbekiston",
    "",
    "🇺🇸 USD — MUHIM IQTISODIY YANGILIKLAR",
    "🥇 XAUUSD — oltin uchun kuzatuv",
    ""
]

try:
    response = requests.get(URL, timeout=25)
    response.raise_for_status()
    events = response.json()

    found = 0

    for event in events:
        if event.get("country") != "USD":
            continue

        if event.get("impact") not in ("High", "Medium"):
            continue

        raw_date = event.get("date", "")

        try:
            event_time = datetime.fromisoformat(
                raw_date.replace("Z", "+00:00")
            )

            if event_time.tzinfo is None:
                event_time = event_time.replace(tzinfo=NY)

            event_time = event_time.astimezone(UZ)

        except (ValueError, TypeError):
            continue

        if event_time.date() != today:
            continue

        found += 1
        impact = event.get("impact", "Noma’lum")
        title = event.get("title", "Noma’lum yangilik")

        message.extend([
            f"{'🔴' if impact == 'High' else '🟠'} {title}",
            f"🕒 Vaqt: {event_time:%H:%M}",
            f"📊 Prognoz: {event.get('forecast') or 'Yo‘q'}",
            f"📉 Oldingi: {event.get('previous') or 'Yo‘q'}",
            ""
        ])

    if found == 0:
        message.append("Bugun USD bo‘yicha muhim yangilik topilmadi.")

    message.extend([
        "",
        "⚠️ Yangilik ta’siri oldindan kafolatlanmaydi.",
        "Manba: Forex Factory kalendar ma’lumotlari."
    ])

except Exception as error:
    message.extend([
        "⚠️ Iqtisodiy kalendarni olishda xato yuz berdi.",
        str(error)[:250]
    ])

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

result = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": "\n".join(message)
    },
    timeout=25
)

result.raise_for_status()
print(result.text)
