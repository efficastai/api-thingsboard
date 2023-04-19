import psycopg2
from datetime import datetime


class DBConection:
    def __init__(self, database, username, password, host, port):
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.database,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except Exception as e:
            print("""Unable to connect to the database: """, e)

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from the database")

    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print("Unable to execute the query: ", e)
