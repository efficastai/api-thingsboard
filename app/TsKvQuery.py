from .PostgresDB import *
from datetime import datetime


class TsKvQuery:

    def __init__(self, device=None, alias=None):
        self.device = device
        self.alias = alias
        self.db = PostgresDB("thingsboard", "postgres", "sm3inv77i3", "localhost", "5432")
        self.db.connect()

    def __del__(self):
        self.db.disconnect()

    def acumulador_ppm_diario(self, device):
        date = datetime.now()
        month_str = date.strftime('%m')
        date_str = date.strftime('%Y-%m-%d')
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_{date.year}_{month_str} t JOIN device d ON t.entity_id = d.id WHERE "
            f"date_trunc('day', to_timestamp(ts/1000)) = '{date_str}' AND t.key = 36 AND d.name = {device}")
        return result
