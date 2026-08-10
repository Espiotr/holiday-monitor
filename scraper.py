from playwright.sync_api import sync_playwright
from logger import log


class HolidayScraper:

    def __init__(self):
        self.browser = None
        self.page = None


    def start(self):

        log("Start przeglądarki")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=300
        )
        )

        self.page = self.browser.new_page()


    def stop(self):

        log("Zamykam przeglądarkę")

        self.browser.close()
        self.playwright.stop()


    def build_url(self, config):

        url = (
            "https://www.holidaycheck.ch/dh/hotels-tuerkische-riviera/"
            "b2272a4a-632a-3d45-ac37-389c895ecc74"
        )

        params = (
            f"?airport={config['departure_airport']}"
            f"&availability=1"
            f"&directflight=1"
            f"&departuredate={config['departure_date']}"
            f"&returndate={config['return_date']}"
            f"&rooms=a-a-c"
            f"&travelkind=package"
        )

        return url + params



    def open_search(self, config):

        url = self.build_url(config)

        log("Otwieram stronę")
 
        self.page.goto(url)

        self.page.wait_for_timeout(5000)

        log("Sprawdzam cookies")

        cookie_clicked = False

        # Sprawdzamy główną stronę oraz wszystkie iframe
        for frame in self.page.frames:

            try:
                button = frame.locator(
                    "button[aria-label='Annehmen']"
                )

                if button.count() > 0:
                    button.first.click(timeout=5000)

                    log("Cookies zaakceptowane - Annehmen")

                    cookie_clicked = True
                    break

            except:
                pass

            try:
                button = frame.locator(
                    "button[aria-label='Akzeptieren']"
                )

                if button.count() > 0:
                    button.first.click(timeout=5000)

                    log("Cookies zaakceptowane - Akzeptieren")

                    cookie_clicked = True
                    break

            except:
                pass
 
        if not cookie_clicked:
            log("Cookies brak")

        self.page.wait_for_timeout(3000)




    def set_travelers(self, config):

        log("Ustawiam podróżnych")


        try:
            self.page.get_by_label(
                "Reiseteilnehmer & Zimmer"
            ).click()

            self.page.wait_for_timeout(2000)


            children = config.get("children", [])


            for child in children:

                self.page.get_by_test_id(
                    "children-inc-btn"
                ).click()

                self.page.wait_for_timeout(1000)


                age = child["age"]


                clicks = max(age - 1, 0)


                for _ in range(clicks):

                    self.page.get_by_test_id(
                        "child-inc-age-btn"
                    ).click()

                    self.page.wait_for_timeout(500)



            self.page.get_by_test_id(
                "submit-button"
            ).click()


            self.page.wait_for_timeout(3000)


            log("Podróżni ustawieni")


        except Exception as e:

            log(f"Problem z podróżnymi: {e}")


    def select_hotel(self, hotel_name):

        log(f"Wybieram hotel: {hotel_name}")

        self.page.locator(
            "div.react-autosuggest__input"
        ).click()

        self.page.wait_for_timeout(1000)

        self.page.keyboard.type(hotel_name)

        self.page.wait_for_timeout(3000)

        log("Wybieram sugestię hotelu")

        self.page.locator(
            "button.destination-search-suggestion"
        ).first.click()

        self.page.wait_for_timeout(5000)

        log("Klikam Angebote")

        try:
            self.page.get_by_role(
                "button",
                name="Angebote"
            ).first.click(timeout=10000)

        except:
            log("Brak przycisku Angebote - przechodzę dalej")

        self.page.wait_for_timeout(8000)



    def get_price(self):

        log("Szukam ceny")

        self.page.wait_for_timeout(5000)

        import re

        body = self.page.locator("body").inner_text()


        numbers = re.findall(
            r"\d[\d\.]*\sCHF",
            body
        )


        prices = []


        for n in numbers:

            value = n.replace("CHF", "")
            value = value.replace(".", "")
            value = value.strip()


            if value.isdigit():

                value = int(value)


                # tylko realne ceny wyjazdu
                if 1500 <= value <= 4000:

                    prices.append(value)



        print("Wszystkie ceny:", prices[:50])


        if len(prices) >= 3:

            # pierwsze trzy to Liberty Lara
            liberty_prices = prices[:3]


            print(
                "Liberty Lara ceny:",
                liberty_prices
            )


            price = min(liberty_prices)


            print(
                "Cena Liberty Lara:",
                price,
                "CHF"
            )


            return price



        print("Nie znaleziono ceny")

        return None