import logging
import datetime
from pydal import DAL, Field


class database():


    def __init__(self, _db_type: str, _host: str, _user: str, _password: str, _dbname: str):
        self.db_type = _db_type
        self.host = _host
        self.user = _user
        self.password = _password
        self.dbname = _dbname
        self.db_instance = None
        self.create_table()


    def __del__(self):
        if self.db_instance is not None:
            self.db_instance.close()
    

    def get_connection(self):
        if self.db_type == "sqlite":
            return self.db_type + "://" + self.dbname + ".db"
        elif self.db_type in ["mongodb", "mysql"]:
            return self.db_type + "://" + self.user + ":" + self.password + "@" + self.host + "/" + self.dbname
  

    def connect(self):
        if self.db_instance is None:
            try:
                self.db_instance = DAL( self.get_connection() )
            except (pydal.exceptions.NotAuthorizedException) as e:
                logging.error(e.args[1])


    def create_table(self):
        self.connect()

        self.db_instance.define_table(
            'products', 
            Field('name', required=True, default=""),
            Field('url', required=True, default="", unique=True),
            Field('shop', required=True, default="")
            )

        self.db_instance.define_table(
            'prices', 
            Field('product_id', "reference products", required=True, default="", ondelete='CASCADE'),
            Field('price', type="double", required=True, default=""),
            Field('time', type="datetime", required=True, default=datetime.datetime.now())
            )


    def get_products(self):
        self.connect()
        try:
            return self.db_instance().select( self.db_instance.products.ALL )
        except:
            logging.error('Unable to fetch data')


    def get_prices(self, _product_id):
        self.connect()
        try:
            return self.db_instance( self.db_instance.prices.product_id == _product_id ).select()
        except:
            logging.error('Unable to fetch data')

    
    def insert_products(self, _name, _url, _shop):
        self.connect()
        try:
            self.db_instance.products.validate_and_insert( name=_name, url=_url, shop=_shop )
        except:
            logging.error('Unable to insert data')


    def insert_price(self, _id, _price):
        self.connect()
        try:
            self.db_instance.prices.validate_and_insert( product_id=_id, price=_price )
        except:
            logging.error('Unable to insert data')


    def is_cheapest(self, _product_id, _last_price):
        self.connect()
        try:
            if  len(self.db_instance( self.db_instance.prices.product_id == _product_id ).select()) < 1:
                return False
            return _last_price < self.db_instance( self.db_instance.prices.product_id == _product_id ).select().last().price
        except:
            logging.error('Unable to compare prices')
