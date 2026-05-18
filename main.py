import requests
from bs4 import BeautifulSoup
import time

BOT_TOKEN = "IEVIETO_SAVU_TELEGRAM_TOKEN"
CHAT_ID = "IEVIETO_SAVU_CHAT_ID"

URL = "IEVIETO_SAVU_SS_LV_LINKU"

seen = set()

def send(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

while True:
    try:
        r = requests.get(URL, headers={
            "User-Agent": "Mozilla/5.0"
        })

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.select("a.am")

        for link in links:
            href = link.get("href")

            if href and "/msg/" in href:
                full = "https://www.ss.lv" + href

                if full not in seen:
                    seen.add(full)

                    send(f"🏠 Jauns dzīvoklis\n\n{full}")

        time.sleep(300)

    except Exception as e:
        print(e)
        time.sleep(60)
