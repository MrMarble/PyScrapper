from datetime import datetime


class Shop:
    def __init__(self, _id, _url: str):
        self.url = _url
        self.id = _id
        self.timestamp = int(datetime.timestamp(datetime.today()))
        self.price = 0.0

    def get_time(self):
        today = datetime.fromtimestamp(self.timestamp)
        return '{}/{}/{}'.format(today.day, today.month, today.year)
