import configparser
from .PostgresDB import *
from datetime import datetime


class PostgresQuery:
    """
    Esta clase realiza consultas SQL a la base de datos de Thingsboard
    """

    # Variables de clase para la información de la configuración de la base de datos
    config = configparser.ConfigParser()
    config.read('config.ini')
    database_config = config['database']
    database = database_config.get('dbname')
    username = database_config.get('username')
    password = database_config.get('password')
    host = database_config.get('host')
    port = database_config.getint('port')

    def __init__(self, device=None, alias=None):
        self.device = device
        self.alias = alias

        # Inicio la instancia de la base de datos
        self.db = PostgresDB(
            database=self.database,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.db.connect()

        # Creo un objeto datetime para almacenar la fecha y el mes actual
        self.date = datetime.now()
        self.month_str = self.date.strftime('%m')
        self.date_str = self.date.strftime('%Y-%m-%d')

    def __del__(self):
        self.db.disconnect()

    def get_ppm_day_accumulator(self, device):
        """
        Obtenemos el acumulado del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device:
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_'{self.date.year}'_'{self.month_str}' t JOIN device d ON t.entity_id = d.id "
            f"WHERE date_trunc('day', to_timestamp(ts/1000)) = '{self.date_str}' AND t.key= 24 AND d.name = '{device}'"
        )
        print(result)
        return result

    def get_ppm_week_accumulator(self, device):
        """
        Obtenemos el acumulado de la semana, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device:
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id"
            f" WHERE date_trunc('week', to_timestamp(ts/1000)) = date_trunc('week', current_timestamp) AND t.key = 24"
            f" AND d.name = '{device}'"
        )
        return result

    def get_ppm_month_accumulator(self, device):
        """
        Obtenemos el acumulado del mes, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id"
            f" WHERE t.key = 24 AND d.name = '{device}'"
        )
        return result

    def get_ppm_last_n_values(self, device, n):
        """
        Obtenemos el acumulado del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param n: a cuantos valores limitar la consulta
        :param device: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT SUM(long_v) FROM (SELECT long_v FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON"
            f" t.entity_id = d.id WHERE t.key = 24 AND d.name = '{device}' ORDER BY ts DESC LIMIT {n}) AS last_values;"
        )
        return result

    def get_day_pya_values(self, device):
        """
        Comentarios del metodo
        """
        result = self.db.execute_query(
            f"SELECT long_v, ts FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id "
            f"WHERE date_trunc('day', to_timestamp(ts/1000)) = '{self.date_str}' AND t.key = 25 AND d.name = '{device}'"
        )
        return result

    def get_day_ppm_values(self, device):
        """
        Obtenemos una tupla de tuplas con los valores de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device:
        :return: acumulador diario
        """
        result = self.db.execute_query(
            f"SELECT long_v, ts FROM ts_kv_{self.date.year}_{self.month_str} t JOIN device d ON t.entity_id = d.id "
            f"WHERE date_trunc('day', to_timestamp(ts/1000)) = '{self.date_str}' AND t.key = 24 AND d.name = '{device}'"
        )
        return result
