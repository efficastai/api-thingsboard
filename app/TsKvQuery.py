import configparser
from .PostgresDB import *
from datetime import datetime


class TsKvQuery:
    """
    Esta clase realiza consultas SQL a la base de datos de Thingsboard
    """

    def __init__(self, device=None, alias=None):
        # Incluyendo device y alias, por el momento lo tomo desde el metodo
        self.device = device
        self.alias = alias
        # Creo nuevo objeto configparse para utilizar archivo de configuracion
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.database = self.config.get('database', 'dbname')
        self.username = self.config.get('database', 'username')
        self.password = self.config.get('database', 'password')
        self.host = self.config.get('database', 'host')
        self.port = self.config.get('database', 'port')
        # Inicio instancia de la base de datos
        self.db = PostgresDB(self.database, self.username, self.password, self.host, self.port)
        self.db.connect()
        # Creando nuevo objeto date: almaceno mes y fecha completa para utilizar en los
        # metodos que realizan consultas SQL
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

    def get_last_n_values(self, device, n):
        """
        Obtenemos el acumulado del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param n: a cuantos valores limitar la consulta
        :param device: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM (SELECT long_v FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON"
            f" t.entity_id = d.id WHERE t.key = 36 AND d.name = '{device}' ORDER BY ts DESC LIMIT {n}) AS last_values;"
        )
        return result

    def get_all_pya_values(self, device):

        result = self.db.execute_query(
            f"SELECT long_v, ts FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id WHERE"
            f" t.key = 34 AND d.name = '{device}' ORDER BY ts DESC"
        )
        return result
