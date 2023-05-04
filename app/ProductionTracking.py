from .PostgresQuery import *
from .Setting import *
from .SQLiteQuery import *


class ProductionTracking:
    """
    Esta clase esta destinada a llamar a las consultas que devuelvan valores acumulados de ciertos periodos
    y retornar dichos objetos de forma ordenada
    """

    def __init__(self):
        self.query = PostgresQuery()
        self.sqlite_query = SQLiteQuery()

    def get_production_tracking_analysis(self, device, flag=None, target=None, cycle_time=None, machine_state=None,
                                         client=None):
        """
        Método central de la clase. Este método se encarga de recopilar todas los calculos necesarios
        para tener el tracking de la producción de las máquinas. Me refiero: obtenemos todos los valores
        acumulados (dia, semana, mes, ultimos n valores), el porcentaje de cumplimiento en base al target (objetivo
        de producción diario), la tasa de producción instantánea (ultimos 10 valores * 6), performance
        (objetivo de cumplimiento de tasa de producción instantánea en base al objetivo de producción por hora)

        Parametros:
        - device: el nombre del dispositivo
        - flag (opcional): un identificador de ajuste de valores
        - target (opcional): objetivo de piezas diario
        - cycle_time (opcional): objetivo de piezas por hora

        Retorno:
        - Un objeto JSON con el acumulado del dia, semana y mes
        """
        # Obtengo los acumulados del día, la semana, el mes, y los ultimos n valores
        day_accumulator, week_accumulator, month_accumulator, last_n_values = self.get_accumulators(device, flag)
        # Tasa de produccion instantanea
        production_rate = last_n_values * 6
        # Porcentaje de cumplimiento de piezas diario del dispositivo (si existe target seteado, sinó SET)
        daily_compliance_percentege = self.get_daily_compliance_percentage(day_accumulator, target)
        # Porcentaje de performance de la maquina (si existe tiempo de ciclo seteado, sinó SET)
        performance = self.get_performance(production_rate, cycle_time)
        self.insert_machine_state(client, device, machine_state)
        machines_on, machines_off, total_machines = self.get_machines_status(device, client, machine_state)

        result = {
            'api_day_accumulator': day_accumulator,
            'api_week_accumulator': week_accumulator,
            'api_month_accumulator': month_accumulator,
            'api_last_n_values': last_n_values,
            'api_daily_compliance_percentege': daily_compliance_percentege,
            'api_instantaneous_production_rate': production_rate,
            'api_performance': performance,
            'api_machines_on': machines_on,
            'api_machines_off': machines_off,
            'api_total_machines': total_machines
        }

        return result

    def get_accumulators(self, device, flag=None):
        """
        Método que devuelve los acumuladores que necesitamos por el momento (day, week, month, last n values).
        Además, este método identifica a través del flag si los valores necesitan algún tipo de ajuste
        para encajar con las unidades de medida que utiliza la máquina en cuestión.
        Por ejemplo: las soldadoras del tipo s10 necesitan dividir todos sus acumulados por 10, ya qué
        1 ppm equivale a 10 cm de soldadura. Lo mismo sucede en el caso de las s20, en ese caso los valores
        se ajustan a la unidad de medida que necesitan ese tipo de soldadoras.

        Parámetros:
        - device: sobre qué dispositivo hacer la consulta

        Return:
        - day_accumulator, week_accumulator, month_accumulator, last_n_values: los acumuladores que necesitamos
        por el momento
        """
        day_accumulator = int(self.query.get_ppm_day_accumulator(device=device)[0][0])
        week_accumulator = int(self.query.get_ppm_week_accumulator(device=device)[0][0])
        month_accumulator = int(self.query.get_ppm_month_accumulator(device=device)[0][0])
        # Harcodeo para ultimos 10 valores, queda pendiente ingreso por parametro
        last_n_values = int(self.query.get_ppm_last_n_values(device=device, n=10)[0][0])

        if flag is not None:
            setting = Setting()
            day_accumulator, week_accumulator, month_accumulator, last_n_values = setting.fix_values(
                [day_accumulator, week_accumulator, month_accumulator, last_n_values], flag)

        return day_accumulator, week_accumulator, month_accumulator, last_n_values

    @staticmethod
    def get_daily_compliance_percentage(day_accumulator, target):
        """
        Método que devuelve el porcentaje cumplimiento diario del target en el caso que el cliente haya
        ingresado por pantalla un target diario. En caso contrario devolverá set para indicarle que debe
        setear el parámetro

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

    def insert_machine_state(self, client, device, machine_state):
        self.sqlite_query.insert_state(client, device, machine_state)

    def get_machines_status(self, device, client, machine_state):
        machines_on = self.sqlite_query.count_machines_on(client)
        total_machines = self.sqlite_query.count_machines(client)
        machines_off = total_machines - machines_on

        return machines_on, machines_off, total_machines
