import threading

from .PostgresQuery import *
from datetime import datetime


class CustomCalculation:

    def __init__(self):
        self.query = PostgresQuery()
        self.date = datetime.now()
        self.ts_now = self.date.timestamp()
        self.flag = threading.Event()

    def tensar_filter_custom_calculation(self, device, current_data_ts, ppm):
        """
        Comentarios del metodo
        """
        ts = None
        dif = None
        acum_today_pieces = None
        if ppm >= 1:
            self.insert_tensar_data(device, current_data_ts)
            self.flag.wait()
            ts, dif, acum_today_pieces = self.get_last_register(device)

            results = {
                "api_custom_tensar_ts": ts,
                "api_custom_tensar_dif": dif,
                "api_custom_tensar_accumulator": acum_today_pieces
            }
            return results
        return None

    def get_last_register(self, device):
        result = self.query.get_tensar_day_last_register(device)
        return result

    def insert_tensar_data(self, device, current_data_ts):

        try:
            last_ts = self.query.get_tensar_last_ts(device)[0][0]
            print(last_ts)
        except IndexError:
            last_ts = None

        if last_ts is None:
            self.query.insert_tensar_data(self.ts_now, 1, None, device)

        elif last_ts is not None:

            same_day = self.compare_dates_from_timestamp(last_ts)

            if not same_day:
                self.query.insert_tensar_data(self.ts_now, 1, None, device)

            if same_day:
                valid_dif = self.fifteen_minutes_interval(current_data_ts, last_ts)

                if valid_dif is not False:
                    self.query.insert_tensar_data(self.ts_now, 1, valid_dif, device)

    def compare_dates_from_timestamp(self, ts):
        """
        Metodo que compara compara un timestamp con la fecha actual, si coinciden ser del dia de hoy, retorna True
        en caso contrario retorna False
        """
        ts_to_date = ts.date()

        if ts_to_date == self.date:
            return True

        return False

    @staticmethod
    def fifteen_minutes_interval(current_data_ts, last_ts):
        """
        Metodo que comprueba si hay una diferencia mayor a 15 minutos entre el dato actual y el anterior registrado
        en la tabla de Tensar
        """
        dif = current_data_ts - last_ts

        if dif >= 900000:
            return dif

        return False
