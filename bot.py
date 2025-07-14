import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, time as dt_time, timedelta
from rss_feeds import fetch_entries, filter_entries, build_message
from config import TELEGRAM_TOKEN, CHAT_IDS, SCHEDULE_TIME

async def send_updates(bot):
    entries = fetch_entries()
    macro, crypto = filter_entries(entries)
    msg = build_message(macro, crypto)
    for chat_id in CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"❌ Errore invio a {chat_id}: {e}")

async def cmd_notizie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_updates(context.bot)
    await update.message.reply_text("🔄 Notizie inviate!")

async def scheduler(app):
    """Invia le notizie ogni giorno all'ora configurata (SCHEDULE_TIME in UTC)"""
    while True:
        now = datetime.utcnow()
        hh, mm = map(int, SCHEDULE_TIME.split(':'))
        target = datetime.combine(now.date(), dt_time(hour=hh, minute=mm))
        if now > target:
            target += timedelta(days=1)
        wait_seconds = (target - now).total_seconds()
        print(f"[SCHEDULER] Prossima notifica tra {int(wait_seconds)} secondi")
        await asyncio.sleep(wait_seconds)
        await send_updates(app.bot)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("notizie", cmd_notizie))
    
    # Avvia scheduler in background
    asyncio.create_task(scheduler(app))
    
    print(f"[BOT] Avvio bot Telegram...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
