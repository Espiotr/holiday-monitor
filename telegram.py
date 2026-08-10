import urllib.request
import urllib.parse


CHAT_ID = "7285785335"


def send_message(token, message):

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": message
    }).encode()

    urllib.request.urlopen(
        url,
        data=data
    )