from config import Config
from scraper import HolidayScraper
from logger import log
from telegram import send_message
from telegram_config import BOT_TOKEN

config = Config()

scraper = HolidayScraper()


scraper.start()


scraper.open_search(
    config.data
)


scraper.set_travelers(
    config.data
)


for hotel in config.data["hotels"]:

    print()
    print("==========", hotel, "==========")

    scraper.select_hotel(hotel)

    price = scraper.get_price()

    print("HOTEL:", hotel)
    print("CENA:", price, "CHF")


print(
    "AKTUALNA CENA:",
    price,
    "CHF"
)


# odczyt starej ceny

try:
    with open("price.txt", "r") as file:
        old_price = int(file.read())

except:
    old_price = None


print(
    "POPRZEDNIA CENA:",
    old_price,
    "CHF"
)


limit = config.get(
    "price_limit"
)


print(
    "LIMIT CENY:",
    limit,
    "CHF"
)


# zapis nowej ceny

with open("price.txt", "w") as file:
    file.write(
        str(price)
    )


# sprawdzanie ceny

if price <= limit and old_price > limit:

    print(
        "🔥 ALARM! CENA SPADŁA PONIŻEJ LIMITU!"
    )

    send_message(
        BOT_TOKEN,
        f"🔥 ALARM! Liberty Lara: cena {price} CHF. Limit: {limit} CHF."
    )

elif old_price != price:

    print(
        "Cena zmieniła się"
    )

    send_message(
        BOT_TOKEN,
        f"📉 Liberty Lara: cena zmieniła się z {old_price} CHF na {price} CHF."
    )

else:

    print(
        "Cena bez zmian"
    )

scraper.stop()


