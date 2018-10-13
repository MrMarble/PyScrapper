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

    def __del__(self):
        if self.mysql is not None:
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
        products = ("CREATE TABLE IF NOT EXIST products ("
                    "id INT NOT NULL AUTO_INCREMENT"
                    "name VARCHAR(100) NOT NULL DEFAULT '',"
                    "url VARCHAR(255) NOT NULL DEFAULT '',"
                    "shop VARCHAR(100) NOT NULL DEFAULT '',"
                    "PRIMARY KEY(product_id))")
        prices = ("CREATE TABLE IF NOT EXIST prices ("
                  "product_id INT,"
                  "price FLOAT NOT NULL DEFAULT -1.0,"
                  "time DATETIME NOT NULL,"
                  "FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE)")
        self.cursor.execute(products)
        self.cursor.execute(prices)
        self.mysql.commit()
