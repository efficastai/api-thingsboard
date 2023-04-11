from app import PostgresDB
from datetime import datetime


class TsKvQuery:

    def __init__(self, device=None, alias=None):
        self.device = device
        self.alias = alias
        self.db = PostgresDB("thingsboard", "postgres", "sm3inv77i3", "localhost", "5432")

    def acumulador_ppm_diario(self):
        date = datetime.now()
        self.db.connect()
        result = self.db.execute_query(f"SELECT long_v FROM ts_kv_{date.year}_{date.month}")
        self.db.disconnect()
        return
