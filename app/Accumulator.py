from .Query import *


class Accumulator:
    """
    Esta clase esta destinada a llamar a las consultas que devuelvan valores acumulados de ciertos periodos
    y retornar dichos objetos de forma ordenada
    """

    def __init__(self, device):
        self.query = Query()

    def get_accumulators(self, device):
        """
        Metodo que devuelve los acumulados del día, la semana y el mes. Declarada para agregar llamados de manera
        facil en proximas consultas o consultas con mas parametros

        Parametros esperados:
        - device: el nombre del dispositivo

        Retorno:
        - Un objeto JSON con el acumulado del dia, semana y mes
        """
        day_accumulator = self.query.get_today_accumulator(device=device)[0][0]
        week_accumulator = self.query.get_week_accumulator(device=device)[0][0]
        month_accumulator = self.query.get_month_accumulator(device=device)[0][0]

        result = {
            'api_day_accumulator': day_accumulator,
            'week_accumulator': week_accumulator,
            'month_accumulator': month_accumulator
        }

        return result
