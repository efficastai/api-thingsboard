import configparser
from .SQLiteDB import *


class SQLiteQuery:
    """
    Esta clase realiza consultas SQL a la base de datos SQLite
    """

    # Variables de clase para la información de la configuración de la base de datos
    config = configparser.ConfigParser()
    config.read('config.ini')
    sqlite_config = config['sqlite']
    path = sqlite_config.get('path')

    def __init__(self):
        self.db = SQLiteDB(self.path)
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

    def count_machines_on(self, client):
        query = (
            "SELECT COUNT(state) "
            "FROM machines "
            "WHERE state = 1"
            "AND client = {} "
        ).format(client)
        result = self.db.execute_query(query)
        return result

    def count_machines(self, client):
        query = (
            "SELECT COUNT(id) "
            "FROM machines "
            "WHERE client = {} "
        ).format(client)
        result = self.db.execute_query(query)
        return result
