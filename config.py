import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # devi impostare questa variabile su Railway
CHAT_IDS = list(map(int, os.getenv("CHAT_IDS", "").split(',')))  # es: "12345678,87654321"


