import schedule
import time
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
from rss_feeds import fetch_entries, filter_entries, build_message
from config import TELEGRAM_TOKEN, CHAT_IDS, SCHEDULE_TIME

bot = Bot(token=TELEGRAM_TOKEN)

async def send_updates():
    entries = fetch_entries()
    macro, crypto = filter_entries(entries)
    msg = build_message(macro, crypto)
    for chat_id in CHAT_IDS:
        try:
            bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"❌ Errore invio a {chat_id}: {e}")

async def cmd_notizie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_updates()
    await update.message.reply_text("🔄 Notizie inviate!")

def run():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("notizie", cmd_notizie))
    schedule.every().day.at(SCHEDULE_TIME).do(lambda: app.create_task(send_updates()))
    print(f"[SCHEDULER] Notizie giornaliere alle {SCHEDULE_TIME} UTC")
    app.run_polling()

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    run()
