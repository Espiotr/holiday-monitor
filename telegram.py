import urllib.request
import urllib.parse
import os

CHAT_ID = "7285785335"


def send_message(token, message):

    # jeśli token nie został podany, pobierz go z GitHub Secret
    if not token:
        token = os.environ.get("BOT_TOKEN")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": message
    }).encode()

    urllib.request.urlopen(
        url,
        data=data
    )