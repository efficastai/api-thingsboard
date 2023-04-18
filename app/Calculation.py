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
        Este metedo devuelve: tiempo encendido, tiempo apagado, y disponibilidad de una maquina en lo que va
        del dia actual
        """
        # Primero obtengo en una tupla de tuplas todos los valores de pya del dia actual
        pya_vales_current_day = self.query.get_all_pya_values(device=device)
        # Calculo los tiempos de encendido, y tiempos de apagado del dia
        time_on_off_current_day = self.calculate_time_values(pya_vales_current_day)
        time_on = time_on_off_current_day[0]
        time_off = time_on_off_current_day[1]
        # Convierto el string de shift_start en timestamp miliseconds
        shift_to_timestamp_milis = self.shift_to_timestamp_milis(shift_start)
        # Paso los valores al metodo que calcula los ratios
        ratio_shift_time = self.ratio_shift_time(time_on, shift_to_timestamp_milis)

        json = {'time_on': time_on, 'time_off': time_off, 'ratio_shift_time': ratio_shift_time}

        return json

    @staticmethod
    def calculate_time_values(pya_tuple):
        """
        Este metodo retorna una tupla con el total de tiempo encendido (time_on_millis) en [0] y
        el total de tiempo apagado (time_off_milis) [1]
        """
        time_on_milis = 0
        time_off_milis = 0
        last = None
        # Ordeno los valores de timestamp de menor a mayor
        pya_tuple_ordered = sorted(pya_tuple, key=lambda x: x[1])

        # Iterar tupla de pya (pya, ts)
        for i in pya_tuple_ordered:
            if last is None:
                last = i
                continue

            time_diff = i[1] - last[1]
            delta = i[0] - last[0]

            if i[0] == 1 and delta == 0:
                time_on_milis += time_diff

            if i[0] == 0 and delta == -1:
                time_on_milis += time_diff

            if i[0] == 0 and delta == 0:
                time_off_milis += time_diff

            if i[0] == 1 and delta == 1:
                time_off_milis += time_diff

            last = i

        return time_on_milis, time_off_milis

    def ratio_shift_time(self, time_on_milis, shift_to_timestamp_milis=None):
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
