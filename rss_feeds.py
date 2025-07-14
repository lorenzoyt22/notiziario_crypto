import requests
import feedparser

RSS_URLS = [
    "https://some-rss-feed-url.com/rss",
]

def fetch_entries():
    entries = []
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        entries.extend(feed.entries)
    return entries

def filter_entries(entries):
    macro = [e for e in entries if "macro" in e.title.lower()]
    crypto = [e for e in entries if "crypto" in e.title.lower()]
    return macro, crypto

def build_message(macro, crypto):
    msg = "*Macro News*\n"
    for e in macro[:5]:
        msg += f"- [{e.title}]({e.link})\n"
    msg += "\n*Crypto News*\n"
    for e in crypto[:5]:
        msg += f"- [{e.title}]({e.link})\n"
    return msg
