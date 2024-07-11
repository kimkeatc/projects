
from misc import get_alphabets, get_headers
from bs4 import BeautifulSoup
from pprint import pprint
from car import Car
import requests
import logging
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class _CarLogos:

    cars = {}

    def __init__(self) -> None:
        self.alphabet = None

    def _init_result(self, alphabet: str = None, url: str = "") -> None:

        if alphabet is not None:
            self.alphabet = alphabet

        self.cars[self.alphabet] = {
            "cars": [],
            "count": 0,
            "url": url,
        }

    def add_car(self, name: str, url: str):
        car = Car(name, url)
        self.cars[self.alphabet]["cars"].append(vars(car))
        self.cars[self.alphabet]["count"] += 1


class CarLogos(_CarLogos):

    url = "https://www.carlogos.org"

    def __init__(self, alphabets: list = get_alphabets()) -> None:
        super().__init__()

        self.alphabets = alphabets
        self._load_cars()

    def _load_cars(self) -> None:

        for index, alphabet in enumerate(self.alphabets, start=1):
            logging.warning(f"#{index:02d} Loading cars started with alphabet of {alphabet}")

            # Initialize alphabet result
            url = self.get_alphabet_url(alphabet)
            self._init_result(alphabet, url)

            # Send request
            while True:
                try:
                    response = requests.get(url, headers=get_headers(), verify=False)
                    response.raise_for_status()
                    content = response.text
                    break
                except Exception:
                    logging.warning("Retry...")

            # Initialize beautiful soup
            soup = BeautifulSoup(content, features="lxml")
            for car in soup.body.find("ul", attrs={"class": "logo-list"}).find_all("li"):
                name = car.next.contents[1]
                img = car.next.next["src"]
                self.add_car(name, f"{self.url}{img}")

    def get_alphabet_url(self, alphabet: str, *, url: str = "") -> str:
        url = f"{self.url}/start-with-{alphabet}"
        return url


if __name__ == "__main__":

    cls = CarLogos()
    pprint(cls.cars)
