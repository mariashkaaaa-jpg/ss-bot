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

BOT_TOKEN = "8717145220:AAHOXlgEFFw7nr9Z5ijbm17MQWu8jnN5Nho"
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
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if not href:
                continue

            if "/msg/" not in href:
                continue

            full = "https://www.ss.lv" + href

            if full in seen:
                continue

            seen.add(full)

            with open("seen.txt", "a") as f:
                f.write(full + "\n")

            send(f"🏠 Jauns sludinājums\n\n{full}")

        time.sleep(300)

    except Exception as e:

        print(e)

        time.sleep(60)
