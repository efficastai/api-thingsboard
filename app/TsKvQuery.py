from .PostgresDB import *
from datetime import datetime


class TsKvQuery:
    """
    Esta clase realiza consultas SQL a la base de datos de Thingsboard
    """

    def __init__(self, device=None, alias=None):
        self.device = device
        self.alias = alias
        self.db = PostgresDB("thingsboard", "postgres", "sm3inv77i3", "localhost", "5432")
        self.db.connect()
        self.date = datetime.now()
        self.month_str = self.date.strftime('%m')
        self.date_str = self.date.strftime('%Y-%m-%d')

    def __del__(self):
        self.db.disconnect()

    def get_today_accumulator(self, device):
        """
        Obtenemos el acumulado del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device:
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id "
            f"WHERE date_trunc('day', to_timestamp(ts/1000)) = '{self.date_str}' AND t.key = 36 AND d.name = '{device}'"
        )
        return result

    def get_week_accumulator(self, device):
        """
        Obtenemos el acumulado de la semana, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device:
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id"
            f" WHERE date_trunc('week', to_timestamp(ts/1000)) = date_trunc('week', current_timestamp) AND t.key = 36"
            f" AND d.name = '{device}'"
        )
        return result

    def get_month_accumulator(self, device):
        """
        Obtenemos el acumulado del mes, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id"
            f" WHERE t.key = 36 AND d.name = '{device}'"
        )
        return result

    def get_last_values(self, device, n):
        """
        Obtenemos el acumulado del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param n: a cuantos valores limitar la consulta
        :param device: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id"
            f" WHERE t.key = 36 AND d.name = '{device}' ORDER BY t.ts DESC LIMIT {n}"
        )
        return result
