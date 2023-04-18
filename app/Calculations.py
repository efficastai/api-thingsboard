class Calculations:

    def __init__(self):
        pass

    def calculate_time_values(self, tup):
        """
        Este metodo retorna un diccionario con el total de tiempo encendido (time_on_millis) en [0] y
        el total de tiempo apagado (time_off_milis) [1]
        """
        time_on_milis = 0
        time_off_milis = 0
        last = None
        for i in tup:
            print(i[1])
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

    def ratio_shift_time(self, dictionary, shift_period=None):
        ratio_shift_time = 0
        # Retorna el tiempo encendido en [0] y el tiempo apagado en [1]
        times = self.calculate_time_values(dictionary)
        # print(times)
        if times[1] == 0:
            ratio_shift_time = 100
        else:
            ratio_shift_time = times[0] / (times[0] + times[1]) * 100
        # print(type(ratio_shift_time))
        return ratio_shift_time
