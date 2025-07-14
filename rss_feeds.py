import feedparser
import requests
from datetime import datetime, timedelta
from config import RSS_FEEDS, MACRO_KEYWORDS, CRYPTO_KEYWORDS

def fetch_entries():
    entries = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = getattr(entry, 'published_parsed', None)
            if not published: continue
            published_dt = datetime.fromtimestamp(
                feedparser.mktime_tz(published))
            if published_dt.date() == datetime.utcnow().date():
                entries.append({
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": getattr(entry, 'summary', '')[:300]
                })
    return entries

def filter_entries(entries):
    macro = []
    crypto = []
    for e in entries:
        text = (e['title'] + " " + e['summary']).lower()
        if any(k.lower() in text for k in MACRO_KEYWORDS):
            macro.append(e)
        if any(k.lower() in text for k in CRYPTO_KEYWORDS):
            crypto.append(e)
    return macro, crypto

def build_message(macro, crypto):
    msg = "📰 *Notizie del Giorno*\n\n"
    msg += "📈 *Macro / Politiche*:\n"
    if macro:
        for e in macro:
            msg += f"• [{e['source']}] {e['title']}\n{e['link']}\n"
    else:
        msg += "Nessuna notizia rilevante.\n"
    msg += "\n⛓️ *Crypto & Mercato*:\n"
    if crypto:
        for e in crypto:
            msg += f"• [{e['source']}] {e['title']}\n{e['link']}\n"
    else:
        msg += "Nessuna notizia crypto rilevante.\n"
    msg += "\n💡 Usa /notizie per aggiornamenti in qualsiasi momento."
    return msg
