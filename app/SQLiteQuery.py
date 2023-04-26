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

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS machines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client VARCHAR,
                device VARCHAR, 
                state INTEGER
            )
        """
        result = self.db.execute_query(query)
        return result

    def insert_state(self, client, device, state):
        query = """
            INSERT INTO machines (
                client,
                device,
                state
            ) VALUES ('{client}', '{device}', {state})
        """.format(client=client, device=device, state=state)
        self.db.execute_query(query)
