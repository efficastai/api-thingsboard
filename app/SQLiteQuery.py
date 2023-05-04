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
                (SELECT id FROM machines WHERE client = ? AND device = ?),
                ?,
                ?,
                ?
            )
        """
        values = (client, device, client, device, state)
        self.db.execute_query(query, values)

    def count_machines_on(self, client):
        query = (
            "SELECT COUNT(*) "
            "FROM machines "
            "WHERE client = ? "
            "AND state = 1"
        )
        result = self.db.execute_query(query, (client,)).fetchone()[0]
        return result

    def count_machines(self, client):
        query = (
            "SELECT * "
            "FROM machines "
            "WHERE client = ?"
        )
        values = (client,)
        print(values)
        result = self.db.execute_query(query, values).fetchall()
        print("Total maquinas: ".format(result))
        return result
