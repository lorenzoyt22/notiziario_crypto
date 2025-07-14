import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # legge il token dalla variabile d'ambiente
CHAT_IDS = os.getenv('CHAT_IDS', '').split(',')  # es: "123456789,-987654321" diventa lista
SCHEDULE_TIME = "07:00"

RSS_FEEDS = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "The Block": "https://www.theblockcrypto.com/rss",
    "Decrypt": "https://decrypt.co/feed"
}

MACRO_KEYWORDS = ["fed", "fomc", "congress", "trump", "dazi", "tariff", "inflazione", "bce", "ue", "eurozona"]

CRYPTO_KEYWORDS = ["crypto", "bitcoin", "ethereum", "eth", "blockchain", "altcoin", "defi", "nft", "bitcoin fork"]

