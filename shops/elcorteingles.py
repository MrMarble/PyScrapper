import requests
from bs4 import BeautifulSoup
from .shop import Shop


class Elcorteingles(Shop):
    def __init__(self, _id, _url: str):
        super().__init__(_id, _url)
        self.type = 'elcorteingles'
        self.price = self.get_price()

    def get_price(self):
        r = requests.get(self.url, headers= { 'User-Agent': 'PostmanRuntime/7.25.0', 'Accept': '*/*', 'Postman-Token': '6203ea73-80b1-4fbf-9387-f9883ab4c970', 'Host': 'www.elcorteingles.es', 'Connection': 'keep-alive' })
        if r.status_code is 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return float(soup.find('span','current').text.replace('€', ''))
        return -1
