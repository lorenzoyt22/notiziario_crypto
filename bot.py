import os
import time
import feedparser
import requests

# Config da env vars
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

FEED_URL = "https://www.coindesk.com/arc/outboundfeeds/rss/"

# Memorizza link già inviati
sent_articles = set()

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "disable_web_page_preview": True
    }
    try:
        resp = requests.post(url, data=payload, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def fetch_and_send_news():
    feed = feedparser.parse(FEED_URL)
    for entry in feed.entries:
        link = entry.link
        title = entry.title
        if link not in sent_articles:
            msg = f"📰 *{title}*\n{link}"
            send_telegram_message(msg)
            sent_articles.add(link)

if __name__ == "__main__":
    print("Bot notizie crypto avviato...")
    while True:
        fetch_and_send_news()
        time.sleep(600)  # 10 minuti
