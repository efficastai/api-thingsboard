import configparser
from .SQLiteDB import *


class SQLiteQuery:
    """
    Esta clase realiza consultas SQL a la base de datos SQLite
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        sqlite_config = config['sqlite']
        path = sqlite_config.get('path')

        self.db = SQLiteDB(path)
        self.db.connect()

    def __del__(self):
        self.db.disconnect()
