import pymysql
import logging
from pydal import DAL, Field
import datetime


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
            return self.db_type + "://" + self.dbname
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
            Field('url', required=True, default=""),
            Field('shop', required=True, default="")
            )

        self.db_instance.define_table(
            'prices', 
            Field('product_id', "reference products", required=True, default="", ondelete='CASCADE'),
            Field('price', type="double", required=True, default=""),
            Field('time', type="datetime", required=True, default="")
            )


    def get_products(self):
        self.connect()
        try:
            return self.db_instance().select( self.db_instance.products.ALL )
        except:
            logging.error('Unable to fetch data')

    def insert_price(self, _id, _price):
        self.connect()
        try:
            self.db_instance.prices.insert( product_id=_id, price=_price )
        except:
            logging.error('Unable to insert data')
