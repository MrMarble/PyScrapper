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
        self.cursor.execute("""CREATE TABLE IF NOT EXIST `products` (
            `id` int(10) NOT NULL AUTO_INCREMENT
            `name` varchar(100) NOT NULL DEFAULT '',
            `url` varchar(255) NOT NULL DEFAULT '',
            `shop` varchar(100) NOT NULL DEFAULT '',
            PRIMARY KEY(product_id)
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXIST `prices` (
            `product_id` int(10),
            `price` FLOAT NOT NULL DEFAULT -1.0,
            `time` DATETIME NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )""")
        self.mysql.commit()