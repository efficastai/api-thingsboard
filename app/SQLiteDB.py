import sqlite3
from threading import Lock


class SQLiteDB:
    """
    Clase que crea una conexión con una base de datos SQLite
    """
    def __init__(self, database):
        self.database = database
        self.conn = None
        self.lock = Lock()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.database)
            print("Connected to the SQLite database")
        except Exception as e:
            print("Unable to connect to SQLite database")
            raise e

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from SQLite database")

    def execute_query(self, query, value):
        if not self.conn:
            print("No connection to SQLite database")
            return None
        try:
            self.lock.acquire()
            cursor = self.conn.cursor()
            cursor.execute(query, value)
            self.conn.commit()
            return cursor
        except Exception as e:
            print("Unable to execute the SQLite query", e)
            raise e
        finally:
            self.lock.release()
