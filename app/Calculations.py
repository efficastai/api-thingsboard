import math
from datetime import datetime


class Calculations:

    def __init__(self):
        pass

    def calculate_time_values(self, pya_tuple):
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

    def ratio_shift_time(self, pya_tuple, shift_start=None):
        ratio_shift_time = 0
        # Retorna el tiempo encendido en [0] y el tiempo apagado en [1]
        times = self.calculate_time_values(pya_tuple)
        timestamp_now = int(datetime.now().timestamp()) * 1000
        shift_start = self.shift_to_timestamp(shift_start)
        if times[1] == 0:
            ratio_shift_time = 100
        elif shift_start is None:
            ratio_shift_time = math.floor(times[0] / (times[0] + times[1]) * 100)
        else:
            ratio_shift_time = math.floor(times[0] / (timestamp_now - shift_start) * 100)
        # print(type(ratio_shift_time))
        return ratio_shift_time

    @staticmethod
    def shift_to_timestamp_milis(shift_start):
        hour = int(shift_start[:2])
        minutes = int(shift_start[3:])
        now = datetime.now()
        result = int(
            datetime(now.year, now.month, now.day, hour, minutes, now.second).timestamp() * 1000)

        return result
