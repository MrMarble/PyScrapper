import requests
from .shop import Shop
from bs4 import BeautifulSoup


class Amazon(Shop):
    def __init__(self, _name: str, _url: str):
        super().__init__(_name, _url)
        self.type = 'Amazon'
        self.price = self.get_price()

    def get_price(self):
        r = requests.get(self.url)
        if r.status_code is 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return float(soup.find('span', id='priceblock_ourprice').text[4:].replace(',', '.'))
        return -1
