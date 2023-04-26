from .PostgresQuery import *
from .Setting import *


class ProductionTracking:
    """
    Esta clase esta destinada a llamar a las consultas que devuelvan valores acumulados de ciertos periodos
    y retornar dichos objetos de forma ordenada
    """

    def __init__(self):
        self.query = PostgresQuery()

    def get_production_tracking_analysis(self, device, flag=None, target=None, cycle_time=None):
        """
        Metodo que devuelve los acumulados del día, la semana y el mes. Declarada para agregar llamados de manera
        facil en proximas consultas o consultas con mas parametros

        Parametros esperados:
        - device: el nombre del dispositivo

        Retorno:
        - Un objeto JSON con el acumulado del dia, semana y mes
        """
        day_accumulator = int(self.query.get_ppm_day_accumulator(device=device)[0][0])
        week_accumulator = int(self.query.get_ppm_week_accumulator(device=device)[0][0])
        month_accumulator = int(self.query.get_ppm_month_accumulator(device=device)[0][0])
        # Harcodeo para ultimos 10 valores, queda pendiente ingreso por parametro
        last_n_values = int(self.query.get_ppm_last_n_values(device=device, n=10)[0][0])
        # Si los valores necesitan algun tipo de ajuste antes de ser enviados
        if flag is not None:
            setting = Setting()
            day_accumulator, week_accumulator, month_accumulator, last_n_values = setting.fix_values(
                [day_accumulator, week_accumulator, month_accumulator, last_n_values], flag)

        # Tasa de produccion instantanea
        production_rate = last_n_values * 6
        # Porcentaje de cumplimiento de piezas diario del dispositivo (si existe target seteado)
        daily_compliance_percentege = self.get_daily_compliance_percentage(day_accumulator,
                                                                           target) if target is not None else 'Set'

        # Porcentaje de performance de la maquina (si existe cycle_time seteado)
        performance = self.performance(production_rate, cycle_time) if cycle_time is not None else 'Set'

        result = {
            'api_day_accumulator': day_accumulator,
            'api_week_accumulator': week_accumulator,
            'api_month_accumulator': month_accumulator,
            'api_last_n_values': last_n_values,
            'api_daily_compliance_percentege': daily_compliance_percentege,
            'api_instantaneous_production_rate': production_rate,
            'api_performance': performance
        }

        return result

    @staticmethod
    def get_daily_compliance_percentage(day_accumulator, target):
        """
        Método que devuelve el porcentaje cumplimiento diario del target

        Parámetros:
        - day_accumulator: el acumulador del dia
        - target: el target diario seteado
        """
        daily_compliance_percentege = round(day_accumulator * 100 / target)

        return daily_compliance_percentege

    @staticmethod
    def performance(production_rate, cycle_time):
        """
        Metodo que devuelve el porcentaje de rendimiento de la maquina basado en su tasa de produccion
        y el tiempo de ciclo

        Parámetros:
        - production_rate: tasa de produccion instantanea
        - cycle_time: tiempo de ciclo

        Retorno:
        - performance: porcentaje de performance de la maquina
        """
        performance = round(production_rate / cycle_time * 100)

        return performance
