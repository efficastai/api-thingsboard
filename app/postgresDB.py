import psycopg2


class PostgresDB:
    """
    Clase que crea una conexión con la base de datos de Thingsboard.
    """

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
            print("Connected to the database")
        except Exception as e:
            print("""Unable to connect to the database: """, e)

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from the database")

    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            if query.startswith('INSERT') or query.startswith('UPDATE') or query.startswith('DELETE'):
                cursor.execute(query)
                self.conn.commit()
                return None
            else:
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                return result
        except Exception as e:
            print("Unable to execute the query: ", e)
