import requests
from bs4 import BeautifulSoup
from .shop import Shop


class Fnac(Shop):
    def __init__(self, _id, _url: str):
        super().__init__(_id, _url)
        self.type = 'fnac'
        self.price = self.get_price()

    def get_price(self):
        r = requests.get(self.url)
        if r.status_code is 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return float(soup.find('li', 'js-fnacOffersTab').find('span').text[1:].replace(',', '.').replace('€', ''))
        return -1
