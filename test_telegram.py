from telegram import send_message
from telegram_config import BOT_TOKEN

send_message(
    BOT_TOKEN,
    "✅ TEST Holiday Monitor działa!"
)

print("Wiadomość wysłana")