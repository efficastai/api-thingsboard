from datetime import datetime
import math
from .TsKvQuery import *


class Calculation:
    """
    Clase Calculation: Esta clase inicializa calculos variados para las maquinas. En primera instancia la utilizamos
    para llamar al metodo "get_machine_time_calculations" (ver en su descripcion el uso)
    """

    def __init__(self):
        self.query = TsKvQuery()

    def get_machine_time_calculations(self, device, shift_start=None, shift_end=None):
        """
        Este método devuelve el tiempo encendido, tiempo apagado y disponibilidad de una máquina en lo que va
        del día actual.
        """
        # Obtengo los valores de PYA del día actual en una tupla de tuplas.
        pya_values_current_day = self.query.get_all_pya_values(device=device)

        # Calculo los tiempos de encendido y apagado del día.
        time_on, time_off = self.calculate_time_values(pya_values_current_day)

        # Convierto el string de shift_start en un timestamp en milisegundos.
        shift_to_timestamp_millis = self.shift_to_timestamp_milis(shift_start)

        # Calculo los ratios de tiempo para el turno.
        ratio_shift_time = self.ratio_shift_time(time_on, shift_to_timestamp_millis)

        # Devuelvo los resultados como un diccionario JSON.
        json = {
            'api_time_on_current_day': time_on,
            'api_time_off_current_day': time_off,
            'api_ratio_shift_time_current_day': ratio_shift_time,
        }

        return json

    @staticmethod
    def calculate_time_values(pya_tuple):
        """
        Este método retorna una tupla con el total de tiempo encendido (time_on_millis) en [0] y
        el total de tiempo apagado (time_off_milis) [1]
        """
        time_on_milis = 0
        time_off_milis = 0
        last = None

        # Ordenar los valores de timestamp de menor a mayor
        pya_tuple_ordered = sorted(pya_tuple, key=lambda x: x[1])

        # Iterar tupla de pya (pya, ts)
        for pya, ts in pya_tuple_ordered:
            if last is None:
                last = (pya, ts)
                continue

            delta = pya - last[0]
            time_diff = ts - last[1]

            if delta == 0:
                if pya == 1:
                    time_on_milis += time_diff
                elif pya == 0:
                    time_off_milis += time_diff
            elif delta == -1:
                time_on_milis += time_diff
            elif delta == 1:
                time_off_milis += time_diff

            last = (pya, ts)

        return time_on_milis, time_off_milis

    @staticmethod
    def ratio_shift_time(time_on_milis, shift_to_timestamp_milis=None):
        # Retorna el tiempo encendido en [0] y el tiempo apagado en [1]
        timestamp_now = int(datetime.now().timestamp()) * 1000
        if time_on_milis == 0:
            ratio_shift_time = 0
        elif shift_to_timestamp_milis is None:
            ratio_shift_time = math.floor(time_on_milis / timestamp_now * 100)
        else:
            ratio_shift_time = math.floor(time_on_milis / (timestamp_now - shift_to_timestamp_milis) * 100)
        # print(type(ratio_shift_time))
        return ratio_shift_time

    @staticmethod
    def shift_to_timestamp_milis(shift_start):
        hour = int(shift_start[:2])
        minutes = int(shift_start[3:])
        now = datetime.now()
        result = int(
            datetime(now.year, now.month, now.day, hour, minutes, now.second).timestamp()) * 1000

        return result
