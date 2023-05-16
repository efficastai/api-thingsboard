import threading

from .PostgresQuery import *
from datetime import datetime


class CustomCalculation:

    def __init__(self):
        self.query = PostgresQuery()
        self.date = datetime.now()
        self.flag = threading.Event()

    def get_tensar_custom_data(self, device, ts, value, interval):
        """
        Método que determina si es necesario retornar nuevos datos para la tabla personalizada de tensar
        """
        is_valid_value = value >= 1
        ts_int = int(ts)
        interval_to_milis = int(interval) * 60000
        print(interval_to_milis)
        if is_valid_value:
            insert_custom_data = self.insert_tensar_data(device, ts_int, interval_to_milis)
            print(insert_custom_data)
            if insert_custom_data:
                last_register = self.get_tensar_last_register(device)
                print(last_register)
                return last_register

        return None

    def insert_tensar_data(self, device, ts, interval):
        """
        Método que recibe un dispositivo y una estampa de tiempo, luego consulta si existen registros anteriores
        de dicho dispositivo, en caso de que no existan, ingresa el primer registro. Luego realiza otras comprobaciones
        """
        # Valores por defecto a insertar en el registro
        value = 1
        dif = 0
        # Traigo el ultimo registro de timestamp, en caso de que no exista, es None
        try:
            last_ts = self.query.get_tensar_last_ts(device)[0][0]
        except IndexError:
            last_ts = None

        # Si no existe un ultimo registro, inserto el registro actual y retorno True
        if last_ts is None:
            self.query.insert_tensar_data(ts, value, dif, device)
            return True
        elif last_ts is not None:
            is_same_day = self.compare_dates_from_timestamp(ts)
            # Si el registro no es del mismo dia, inserto el dato y retorno True
            if not is_same_day:
                self.query.insert_tensar_data(ts, value, dif, device)
                return True
            elif is_same_day:
                valid_dif = self.is_valid_interval(ts, last_ts, interval)
                # Si es una diferencia de tiempo valida, inserto el dato y retorno True
                if valid_dif is not False:
                    self.query.insert_tensar_data(ts, value, valid_dif, device)
                    return True

        return False

    def get_tensar_last_register(self, device):
        """
        Metodo que retorna un objeto JSON con los resultados obtenidos de la tabla de Tensar:
        ultimo ts y dif registrado, total acumulado de piezas del dia en base a los filtros que requieren ser
        aplicados.

        Parámetros:

        Return:

        """
        ts, dif = self.query.get_tensar_day_last_register(device)[0]
        day_accumulator = self.query.get_tensar_day_accumulator(device)[0][0]

        result = {
            'api_custom_tensar_ts': ts,
            'api_custom_tensar_dif': dif,
            'api_custom_tensar_accumulator': day_accumulator
        }

        return result

    def compare_dates_from_timestamp(self, ts):
        """
        Metodo que compara compara un timestamp con la fecha actual, si coinciden ser del dia de hoy, retorna True
        en caso contrario retorna False
        """
        ts = ts / 1000
        ts_to_date = datetime.fromtimestamp(ts).date()
        if ts_to_date == self.date.date():
            return True

        return False

    @staticmethod
    def is_valid_interval(ts, last_ts, interval):
        """
        Metodo que comprueba si hay una diferencia mayor a 15 minutos entre el dato actual y el anterior registrado
        en la tabla de Tensar
        """
        dif = ts - last_ts

        if dif >= interval:
            return dif

        return False
