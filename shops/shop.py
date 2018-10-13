from datetime import datetime


class Shop:
    def __init__(self, _id, _url: str):
        self.url = _url
        self.id = _id
        self.price = 0.0