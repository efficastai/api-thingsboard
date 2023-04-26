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
        self.db.execute_query(query)

    def insert_state(self, client, device, state):
        query = """
            REPLACE INTO machines (
                id,
                client,
                device,
                state
            ) VALUES (
            (SELECT id FROM machines WHERE client = '{client}' AND device = '{device}'),
            '{client}', 
            '{device}', 
            {state})
        """.format(client=client, device=device, state=state)
        self.db.execute_query(query)
