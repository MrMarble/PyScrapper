import pymysql
import logging


class database():
    def __init__(self, _host: str, _user: str, _password: str, _dbname: str):
        self.host = _host
        self.user = _user
        self.password = _password
        self.dbname = _dbname
        self.mysql = None
        self.cursor: pymysql.cursors.Cursor = None
        self.create_table()

    def __del__(self):
        if self.mysql is not None:
            self.cursor.close()
            self.mysql.close()

    def connect(self):
        if self.mysql is None:
            try:
                self.mysql = pymysql.connect(self.host, self.user, self.password, self.dbname)
                self.cursor = self.mysql.cursor()
            except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
                if type(e) is pymysql.err.OperationalError:
                    logging.error(e.args[1])
                elif type(e) is pymysql.err.InternalError:
                    logging.error(e.args[1])

    def create_table(self):
        self.connect()
        products = """CREATE TABLE IF NOT EXISTS products (
                    id INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL DEFAULT '',
                    url VARCHAR(255) NOT NULL DEFAULT '',
                    shop VARCHAR(100) NOT NULL DEFAULT '',
                    PRIMARY KEY(id))"""
        prices = """CREATE TABLE IF NOT EXISTS prices (
                  product_id INT,
                  price FLOAT NOT NULL DEFAULT -1.0,
                  time DATETIME NOT NULL,
                  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE)"""
        self.cursor.execute(products)
        self.cursor.execute(prices)
        self.mysql.commit()

    def get_products(self):
        self.connect()
        sql = 'SELECT id, shop, url FROM products'
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            logging.error('Unable to fetch data')

    def insert_price(self, _id, _price, _timestamp):
        self.connect()
        sql = 'INSERT INTO prices VALUES({}, {}, {})'.format(_id, _price, _timestamp)
        try:
            self.cursor.execute(sql)
            self.mysql.commit()
        except:
            self.mysql.rollback()
            logging.error('Unable to insert data')
