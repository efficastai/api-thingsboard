import time

from .PostgresQuery import *
from .Setting import *


class ProductionTracking:
    """
    Esta clase esta destinada a llamar a las consultas que devuelvan valores acumulados de ciertos periodos
    y retornar dichos objetos de forma ordenada.
    """

    def __init__(self):
        self.query = PostgresQuery()

    def get_production_tracking_analysis(self, device, fix=None, target=None, cycle_time=None, customer=None):
        """
        Método central de la clase. Recopila los cálculos necesarios para realizar el seguimiento de la producción de
        las máquinas. Esto incluye obtener los valores acumulados (día, semana, mes y últimos n valores), el porcentaje
        de cumplimiento en relación al objetivo diario de producción (target), la tasa de producción instantánea
        (últimos 10 valores multiplicados por 6) y la performance (objetivo de cumplimiento de la tasa de producción
        instantánea en relación al objetivo de producción por hora).

        Parámetros:
        - device: el nombre del dispositivo.
        - flag (opcional): un identificador de ajuste de valores.
        - target (opcional): objetivo de piezas diario.
        - cycle_time (opcional): objetivo de piezas por hora.

        Retorno:
        - Un objeto JSON con los valores acumulados del día, semana y mes.
        """

        # Obtengo los acumulados del día, la semana, el mes, y los ultimos n valores
        day_accumulator, week_accumulator, month_accumulator, last_n_values = self.get_accumulators(device, fix)
        # Tasa de produccion instantanea
        production_rate = last_n_values * 6
        # Porcentaje de cumplimiento de piezas diario del dispositivo (si existe target seteado, sinó SET)
        daily_compliance_percentege = self.get_daily_compliance_percentage(day_accumulator, target)
        # Porcentaje de performance de la maquina (si existe tiempo de ciclo seteado, sinó SET)
        performance = self.get_performance(production_rate, cycle_time)
        # Chequear si borrar la causa de parada de Fundemap
        check_clear_stop_cause = self.check_clear_stop_cause(device, customer, 6)

        result = {
            'api_day_accumulator': day_accumulator,
            'api_week_accumulator': week_accumulator,
            'api_month_accumulator': month_accumulator,
            'api_last_n_values': last_n_values,
            'api_daily_compliance_percentege': daily_compliance_percentege,
            'api_instantaneous_production_rate': production_rate,
            'api_performance': performance,
        }

        if check_clear_stop_cause is not None:
            result = {**result, **check_clear_stop_cause}

        return result

    def get_accumulators(self, device, fix=None):
        """
        Método que devuelve los acumuladores necesarios (día, semana, mes, últimos n valores) para el dispositivo
        especificado.
        También ajusta los valores según el dispositivo, si es necesario, para que coincidan con las unidades de medida
        utilizadas por la máquina.

        Por ejemplo, las soldadoras del tipo S10 requieren dividir todos sus acumulados por 10, ya que 1 ppm equivale
        a 10 cm de soldadura. Del mismo modo, en el caso de las soldadoras S20, los valores se ajustan a la unidad de
        medida requerida por ese tipo de soldadoras.

        Parámetros:
        - device: el dispositivo para el cual se realiza la consulta.

        Retorno:
        - day_accumulator, week_accumulator, month_accumulator, last_n_values: los acumuladores necesarios en el momento
        actual.
        """

        day_accumulator = int(self.query.get_ppm_day_accumulator(device=device)[0][0])
        week_accumulator = int(self.query.get_ppm_week_accumulator(device=device)[0][0])
        month_accumulator = int(self.query.get_ppm_month_accumulator(device=device)[0][0])
        # Harcodeo para ultimos 10 valores, queda pendiente ingreso por parametro
        last_n_values = int(self.query.get_ppm_last_n_values(device=device, n=10)[0][0])

        if fix is not None:
            setting = Setting()
            day_accumulator, week_accumulator, month_accumulator, last_n_values = setting.fix_values(
                [day_accumulator, week_accumulator, month_accumulator, last_n_values], fix)

        return day_accumulator, week_accumulator, month_accumulator, last_n_values

    @staticmethod
    def get_daily_compliance_percentage(day_accumulator, target):
        """
        Método que devuelve el porcentaje cumplimiento diario del target en el caso que el cliente haya
        ingresado por pantalla un target diario. En caso contrario devolverá set para indicarle que debe
        setear el parámetro.

        Parámetros:
        - day_accumulator: el acumulador del dia
        - target: el target diario seteado
        """
        daily_compliance_percentege = round(day_accumulator * 100 / target) if target is not None else 'Set'

        return daily_compliance_percentege

    @staticmethod
    def get_performance(production_rate, cycle_time):
        """
        Metodo que devuelve el porcentaje de rendimiento de la maquina basado en su tasa de produccion
        y el tiempo de ciclo, en el caso donde el cliente haya ingresado un tiempo de ciclo por pantalla.
        En caso contrario devolverá set para indicarle que debe setear el parámetro.

        Parámetros:
        - production_rate: tasa de produccion instantanea
        - cycle_time: tiempo de ciclo

        Retorno:
        - performance: porcentaje de performance de la maquina
        """
        performance = round(production_rate / cycle_time * 100) if cycle_time is not None else 'Set'

        return performance

    def check_clear_stop_cause(self, device, customer, n):
        """
        Método que recibe un cliente (por el momento solamente Fundemap necesita esta característica), realiza
        una consulta a la base de datos para comprobar si los últimos n datos son datos de máquina encendida.
        En el caso de qué lo sean, el método devuelve True, por lo qué en los nodos de Thingsboard, se cambiará
        el tipo de mensaje a POST_ATTRIBUTES_REQUEST y se actualizará la causa de parada para eliminar su contenido.

        Parámetros:
        - device: un dispositivo
        - customer: un cliente
        - n: la cantidad de datos 1 que necesitamos

        Return:
        - Un objeto JSON con stop_cause en True o False
        - None en caso de que el cliente no sea Fundemap
        """
        customer = customer.lower() if customer is not None else None

        if customer == 'fundemap':

            stop_cause = False

            try:
                last_n_pya = int(self.query.get_pya_last_n_values(device, n)[0][0])
            except IndexError:
                last_n_pya = None

            if last_n_pya >= n:
                stop_cause = True

            result = {
                'api_stop_cause': stop_cause
            }

            return result

        return None
