import requests
from bs4 import BeautifulSoup
from .shop import Shop


class Mediamarkt(Shop):
    def __init__(self, _id, _url: str):
        super().__init__(_id, _url)
        self.type = 'mediamarkt'
        self.price = self.get_price()

    def get_price(self):
        r = requests.get(self.url)
        if r.status_code is 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return float(soup.find("meta",  property="product:price:amount")['content'])
        return -1
