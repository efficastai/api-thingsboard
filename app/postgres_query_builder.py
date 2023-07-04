import configparser
from .postgresDB import *
from datetime import datetime
from query import postgres


class PostgreSQLQueryBuilder:
    """
    Esta clase realiza consultas SQL a la base de datos de Thingsboard..
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
        self.year = self.date.year
        self.month_str = self.date.strftime('%m')
        self.date_str = self.date.strftime('%Y-%m-%d')

    def __del__(self):
        self.db.disconnect()

    def get_ppm_day_accumulator(self, entity_id):
        """
        Obtenemos el acumulado del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36).
        :param entity_id:
        :return: acumulador diario
        """
        query = postgres.get('get_ppm_day_accumulator').format(self.year, self.month_str, self.date_str, entity_id)
        result = self.db.execute_query(query)
        return result

    def get_ppm_week_accumulator(self, entity_id):
        """
        Obtenemos el acumulado de la semana, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param entity_id:
        :return: acumulador diario
        """
        query = postgres.get('get_ppm_week_accumulator').format(self.year, self.month_str, entity_id)
        result = self.db.execute_query(query)
        return result

    def get_ppm_month_accumulator(self, entity_id):
        """
        Obtenemos el acumulado del mes, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param entity_id: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        query = postgres.get('get_ppm_month_accumulator').format(self.year, self.month_str, entity_id)
        result = self.db.execute_query(query)
        return result

    def get_pya_day_accumulator(self, entity_id):
        """
        Obtenemos el acumulado del dia de pya
        """
        query = postgres.get('get_pya_day_accumulator').format(self.year, self.month_str, self.date_str, entity_id)
        result = self.db.execute_query(query)
        return result

    def get_ppm_count_day_accumulator(self, device):
        """
        Obtenemos la sumatoria de registros de ppm del dia (registros, no la sumatoria de los valores de ppm)
        """
        query = postgres.get('get_ppm_count_day_accumulator').format(self.year, self.month_str, self.date_str, device)
        result = self.db.execute_query(query)
        return result

    def get_pya_total_accumulator(self, entity_id):
        """
        Obtenemos el acumulado historico de pya
        """
        query = postgres.get('get_pya_total_accumulator').format(entity_id)
        result = self.db.execute_query(query)
        return result

    def get_ppm_last_n_values(self, entity_id, n):
        """
        Obtenemos el acumulado del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param n: a cuantos valores limitar la consulta
        :param entity_id: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        query = postgres.get('get_ppm_last_n_values').format(self.year, self.month_str, entity_id, n)
        result = self.db.execute_query(query)
        return result

    def get_pya_last_n_values(self, entity_id, n):
        """
        A diferencia del metodo de arriba, este método retorna los 5 ultimos registros en formato tupla
        :param n: a cuantos valores limitar la consulta
        :param entity_id: a que dispositivo queremos referenciar
        :return: tupla de ultimos 5 registros pya
        """
        query = postgres.get('get_pya_last_n_values').format(self.year, self.month_str, entity_id, n)
        result = self.db.execute_query(query)
        return result

    def get_pya_last_n_registers_asc(self, entity_id, n):
        """
        Comentarios del metodo
        """
        query = postgres.get('get_pya_last_n_registers_asc').format(self.year, self.month_str, entity_id, n)
        result = self.db.execute_query(query)
        return result

    def get_last_data_ts(self, device):
        """
         Obtenemos el ultimo valor del día, de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param device: a que dispositivo queremos referenciar
        :return: acumulador diario
        """
        query = postgres.get('get_last_data').format(device)
        result = self.db.execute_query(query)
        return result

    def get_day_pya_values(self, entity_id):
        """
        Obtenemos un lista con los valores de pya del dia
        """
        query = postgres.get('get_day_pya_values').format(self.year, self.month_str, self.date_str, entity_id)
        result = self.db.execute_query(query)
        return result

    def get_day_ppm_values(self, entity_id):
        """
        Obtenemos una tupla de tuplas con los valores de la tabla ts_kv_{esteAnio}_{esteMes} en base a los PPM (key 36)
        :param entity_id:
        :return: acumulador diario
        """
        query = postgres.get('get_day_ppm_values').format(self.year, self.month_str, self.date_str, entity_id)
        result = self.db.execute_query(query)
        return result

    def get_device_access_token(self, device):
        """
        Obtenemos el access token de un dispositivo en particular
        """
        query = postgres.get('get_device_access_token').format(device)
        result = self.db.execute_query(query)
        return result

    def get_last_ts_where_ppm_equals_1(self, device):
        """
        Obtenemos el ultimo ts de un dato de ppm >= 1
        """
        query = postgres.get('get_last_ts_where_ppm_equals_1').format(self.year, self.month_str, device)
        result = self.db.execute_query(query)
        return result

    # QUERY DE TENSAR

    def insert_tensar_data(self, ts, pieza, dif, device, counter):
        """
        Insertamos la nueva informacion en la tabla de Tensar.
        """
        query = postgres.get('insert_tensar_data').format(ts, pieza, dif, device, counter)
        self.db.execute_query(query)

    def get_tensar_last_ts(self, device):
        """
        Obtenemos el timestamp del ultimo dato registrado de un determinado dispositivo. Este query esta enfocado
        a ser utilizado en la creacion de la tabla que necesita contar Tensar en base a la diferencia de tiempo entre
        piezas.
        """
        query = postgres.get('get_tensar_last_ts').format(device)
        result = self.db.execute_query(query)
        return result

    def get_tensar_day_last_register(self, device):
        """
        Obtenemos la ultima fila de registro de la tabla tensar
        """
        query = postgres.get('get_tensar_day_last_register').format(device, self.date_str)
        result = self.db.execute_query(query)
        return result

    def get_tensar_day_last_value(self, device):
        """
        Comentarios del metodo
        """
        query = postgres.get('get_tensar_day_last_value').format(device, self.date_str)
        result = self.db.execute_query(query)
        return result

    def update_tensar_last_value(self, value, dif, device):
        """
        Comentarios del metodo
        """
        query = postgres.get('update_tensar_last_value').format(value, dif, device)
        result = self.db.execute_query(query)
        return result

    def count_tensar_values(self, device, value):
        """
        Comentarios del metodo
        """
        query = postgres.get('count_tensar_values').format(device, value, self.date_str)
        result = self.db.execute_query(query)
        return result

    def get_tensar_day_accumulator(self, device):
        """
        Obtenemos el acumulador del dia de la tabla  tensar
        """
        query = postgres.get('get_tensar_day_accumulator').format(device, self.date_str)
        result = self.db.execute_query(query)
        return result

    def get_tensar_week_accumulator(self, device):
        """
        Obtenemos el acumulador semanal de la tabla tensar
        """
        query = postgres.get('get_tensar_week_accumulator').format(device)
        result = self.db.execute_query(query)
        return result

    def get_tensar_month_accumulator(self, device):
        """
        Obtenemos el acumulado mensual de la tabla tensar
        """
        query = postgres.get('get_tensar_month_accumulator').format(device)
        result = self.db.execute_query(query)
        return result

    def get_tensar_last_counter(self, device):
        """
        Comentarios del metodo
        """
        query = postgres.get('get_tensar_last_counter').format(device)
        result = self.db.execute_query(query)
        return result

    def update_tensar_counter(self, device):
        """
        Comentarios del metodo
        """
        query = postgres.get('get_tensar_last_counter').format(device)
        self.db.execute_query(query)