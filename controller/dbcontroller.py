import sqlite3
from sqlite3 import Error

class DbController():
    __conn= None
    def __init__(self, db="data/dissandb.db"):
        try:
            self.__conn= sqlite3.connect(db)
        except Error as e:
            print (e)
    def get_conection(self):
        return self.__conn
    def close_connection(self):
        try:
            self.__conn.close()
            return True
        except:
            return False
    def create_data_structure(self):
        if self.__conn.execute("SELECT name FROM sqlite_master WHERE name='products'").fetchone() is None:
            try:
                self.__conn.execute("CREATE TABLE products(id INTEGER PRIMARY KEY ASC, code TEXT NOT NULL UNIQUE, name TEXT NOT NULL, price REAL NOT NULL, date TEXT NOT NULL, img BLOB)")
                self.__conn.execute("CREATE TABLE user(id INTEGER PRIMARY KEY ASC, mail TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
                self.__conn.commit()
                return True
            except Error as e:
                print(e)
        else:
            return False
    def load_products(self, products, with_img=False):
        sqlvalues=[(prod['id'], prod['default_code'], prod['name_template'].rstrip(" "), prod['list_price'], prod['write_date']) for prod in products]
        self.__conn.executemany('INSERT OR REPLACE INTO products (id, code, name, price, date, img) VALUES (?,?,?,?,?,NULL)', sqlvalues)
        self.__conn.commit()



