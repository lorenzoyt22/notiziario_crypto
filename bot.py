from flask import Flask, request
import os
import requests
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_IDS
from rss_feeds import fetch_entries, filter_entries, build_message

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

def send_updates():
    entries = fetch_entries()
    macro, crypto = filter_entries(entries)
    msg = build_message(macro, crypto)
    for chat_id in CHAT_IDS:
        try:
            bot.send_message(chat_id=int(chat_id), text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"❌ Errore invio a {chat_id}: {e}")

@app.route('/notizie', methods=['GET'])
def cmd_notizie():
    send_updates()
    return "🔄 Notizie inviate!"

if __name__ == '__main__':
    # Avvia Flask sul default port Railway 8000 o usa PORT env
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

