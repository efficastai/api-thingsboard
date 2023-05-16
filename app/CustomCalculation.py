import threading

from .PostgresQuery import *
from datetime import datetime


class CustomCalculation:

    def __init__(self):
        self.query = PostgresQuery()
        self.date = datetime.now()
        self.ts_now = int(self.date.timestamp()) * 1000
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
            ts, dif = self.get_last_register(device)[0]
            acum_today_pieces = self.query.count_tensar_total_pieces(device)[0][0]

        results = {
            "api_custom_tensar_ts": ts,
            "api_custom_tensar_dif": dif,
            "api_custom_tensar_accumulator": acum_today_pieces
        }
        return results

    def get_last_register(self, device):
        result = self.query.get_tensar_day_last_register(device)
        return result

    def insert_tensar_data(self, device, current_data_ts):

        try:
            last_ts = self.query.get_tensar_last_ts(device)[0][0]
            print("ESTOY EN EL LAST! ///// ", last_ts)
        except IndexError:
            print("ERROR DE INDEX!")
            last_ts = None

        if last_ts is None:
            self.query.insert_tensar_data(current_data_ts, 1, 0, device)

        elif last_ts is not None:

            same_day = self.compare_dates_from_timestamp(last_ts)
            print("SAME DAY", same_day)
            if not same_day:
                self.query.insert_tensar_data(current_data_ts, 1, 0, device)

            if same_day:
                valid_dif = self.fifteen_minutes_interval(current_data_ts, last_ts)
                print("VALID DIFFFFF: ", valid_dif)
                if valid_dif is not False:
                    self.query.insert_tensar_data(current_data_ts, 1, valid_dif, device)

    def compare_dates_from_timestamp(self, ts):
        """
        Metodo que compara compara un timestamp con la fecha actual, si coinciden ser del dia de hoy, retorna True
        en caso contrario retorna False
        """
        ts = ts / 1000
        ts_to_date = datetime.fromtimestamp(ts).date()
        print("TIMESTAMP TO DATE: ", ts_to_date)
        print("ESTA FECHA: ", self.date.today())
        if ts_to_date == self.date.today():
            return True

        return False

    @staticmethod
    def fifteen_minutes_interval(current_data_ts, last_ts):
        """
        Metodo que comprueba si hay una diferencia mayor a 15 minutos entre el dato actual y el anterior registrado
        en la tabla de Tensar
        """
        dif = current_data_ts - last_ts

        if dif >= 120000:
            return dif

        return False
