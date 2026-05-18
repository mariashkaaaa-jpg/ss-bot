import requests
from bs4 import BeautifulSoup
import time

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_web():
    app.run(host="0.0.0.0", port=10000)

Thread(target=run_web).start()

BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
CHAT_ID = "-5186118083"

URL = "https://www.ss.lv/lv/real-estate/flats/riga/all/hand_over/filter/"

try:
    with open("seen.txt", "r") as f:
        seen = set(f.read().splitlines())
except:
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

        r = requests.get(
            URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(r.text, "html.parser")

        for row in soup.select("tr"):

            text = row.get_text(" ", strip=True)

            if "EUR" not in text:
                continue

            try:

                parts = text.split()

                price = None

                for part in parts:

                    clean = (
                        part.replace("€", "")
                        .replace("EUR", "")
                        .strip()
                    )

                    if clean.isdigit():

                        num = int(clean)

                        if 100 <= num <= 5000:
                            price = num

                if not price:
                    continue

                # if price < 300 or price > 500:
                #     continue

                rooms = None

                for part in parts:

                    if part in ["1", "2", "3", "4", "5", "6"]:

                        num = int(part)

                        if 1 <= num <= 6:
                            rooms = num

                if not rooms:
                    continue

                # if rooms < 2 or rooms > 3:
                #     continue

                link = row.find("a")

                if not link:
                    continue

                href = link.get("href")

                if not href:
                    continue

                if href.startswith("/"):

                    full = "https://www.ss.lv" + href

                    if full not in seen:

                        seen.add(full)

                        with open("seen.txt", "a") as f:
                            f.write(full + "\n")

                        send(
                            f"🏠 {rooms} istabas | {price} EUR\n\n{full}"
                        )

            except:
                pass

        time.sleep(300)

    except Exception as e:
        print(e)
        time.sleep(60)
