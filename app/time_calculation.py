import math
import re

from .postgres_query_builder import *
from .decorators import mide_tiempo


class TimeCalculation:
    """
    Clase Calculation: Esta clase inicializa calculos variados para las maquinas. En primera instancia la utilizamos
    para llamar al metodo "get_machine_time_calculations" (ver en su descripcion el uso).
    """

    def __init__(self):
        self.query = PostgreSQLQueryBuilder()

    @mide_tiempo
    def get_machine_time_calculations(self, entity_id, shift_start=None, flag=None):
        """
        Este método devuelve el tiempo encendido, tiempo apagado y disponibilidad de una máquina en lo que va
        del día actual en base a su hora de inicio de turno.
        """
        run_stop_values_tuple = None
        # Si tengo un flag en el cuerpo del mensaje convierto a minúsculas
        if flag is not None:
            flag = flag.lower()
            # Si tengo un flag de soldadora obtengo los valores de ppm del día y luego los convierto a valores de pya
            if "s" in flag:
                try:
                    day_ppm_values = self.query.get_day_ppm_values(entity_id)
                except Exception as e:
                    print("Exception en get_machine_time_calculations:", e)
                run_stop_values_tuple = self.convert_to_pya_tuple(day_ppm_values)
        # Si el mensaje viene sin flag obtengo los valores de pya del día
        if run_stop_values_tuple is None:
            run_stop_values_tuple = self.query.get_day_pya_values(entity_id)

        # Convierto el string de shift_start en un timestamp en milisegundos.
        if shift_start is not None:
            shift_start = self.shift_to_timestamp_milis(shift_start)

        # Calculo los tiempos de encendido y apagado del día.
        time_on, time_off = self.calculate_time_values(run_stop_values_tuple, shift_start)

        # Calculo los ratios de tiempo para el turno.
        ratio_shift_time = self.ratio_shift_time(time_on, shift_start)

        # Devuelvo los resultados como un diccionario JSON.
        results = {
            'api_time_on_current_day': time_on,
            'api_time_off_current_day': time_off,
            'api_ratio_shift_time_current_day': ratio_shift_time,
        }

        return results

    def calculate_time_values(self, run_stop_values_tuple, shift_start_in_timestamp_miliseconds=None):
        """
        Recibe una tupla de valores de PYA. En el índice [0] se encuentra el valor y en el índice [1] se encuentra el
        timestamp en milisegundos. Primero, se ordena la lista de menor a mayor. Luego, se itera sobre los elementos y,
        según el valor de su delta, se acumula el tiempo en tiempo_on_milis o tiempo_off_milis.

        Parámetros:
        - tupla_valores: una tupla de valores.

        Retorno:
        - time_on_milis: el tiempo acumulado en milisegundos para el estado de encendido.
        - time_off_milis: el tiempo acumulado en milisegundos para el estado de apagado.
        """

        time_on_milis = 0
        time_off_milis = 0
        last = None

        run_stop_values_ordered = []
        # Ordenar los valores de timestamp de menor a mayor
        try:
            run_stop_values_ordered = sorted(run_stop_values_tuple, key=lambda x: x[1])
        except Exception as e:
            print("Exception en run_stop_values_ordered", e)

        # Si existe un tiempo de inicio de turno, actualizo la lista a partir de ese timestamp de inicio de turno
        if shift_start_in_timestamp_miliseconds is not None:
            run_stop_values_ordered = self.update_list_from_shift_start(run_stop_values_ordered,
                                                                        shift_start_in_timestamp_miliseconds)

        # Iterar tupla de pya (pya, ts)
        for pya, ts in run_stop_values_ordered:
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
    def ratio_shift_time(time_on_milis, shift_start):
        """
        Calcula el ratio de encendido/apagado de una máquina en base a la hora de inicio del turno. Si no se especifica
        una hora de inicio del turno, el ratio se calculará en función de las horas transcurridas del día.

        Parámetros:
        - tiempo_on_total: el tiempo total encendido de la máquina en milisegundos.
        - hora_inicio_turno (opcional): la hora de inicio del turno en formato HH:MM.

        Retorno:
        - El ratio de tiempo encendido de la máquina durante el día.

        """
        now = datetime.now()
        today = datetime(now.year, now.month, now.day)
        delta = now - today
        today_miliseconds = delta.total_seconds() * 1000
        if time_on_milis == 0:
            ratio_shift_time = 0
        elif shift_start is None:
            ratio_shift_time = round(time_on_milis / today_miliseconds * 100)
        else:
            timestamp_milis = now.timestamp() * 1000
            diff = timestamp_milis - shift_start
            ratio_shift_time = round(time_on_milis / diff * 100)
        return ratio_shift_time

    def shift_to_timestamp_milis(self, shift_start):
        """
        Recibe una cadena de texto que representa una hora de inicio de un turno, convierte la cadena en horas y
        minutos, y luego la devuelve en formato de timestamp en milisegundos.

        Parámetros:
        - hora_turno: una cadena de texto que representa la hora de inicio del turno.

        Retorno:
        - hora_timestamp: la hora de inicio del turno convertida a timestamp en milisegundos, como un entero.
        """

        # Valido que la hora ingresada tenga un formato correcto, en caso de que no, retorno None
        valid = self.validate_shift_format(shift_start)
        if not valid:
            return None
        hour = int(shift_start[:2])
        minutes = int(shift_start[3:])
        now = datetime.now()
        result = int(
            datetime(now.year, now.month, now.day, hour, minutes, now.second).timestamp()) * 1000

        return result

    @staticmethod
    def validate_shift_format(shift):
        """
        Metodo para validar que la hora de turno tenga un formato y unos valores correctos

        Parámetros:
        - shift: un turno en formato string

        Return:
        - None: si el formato de la hora no es correcto
        - result: si el formato esta bien, retorna ese turno en timestamp
        """
        # Comprobar si el formato es hh:mm
        if not re.match(r'^\d{2}:\d{2}$', shift):
            return False
        # Obtener la hora y los minutos como números enteros
        hora, minuto = map(int, shift.split(':'))
        # Comprobar si la hora está entre 00 y 23
        if hora < 0 or hora > 23:
            return False
        # Comprobar si los minutos están entre 00 y 59
        if minuto < 0 or minuto > 59:
            return False
        # Comprobar si los dos puntos están en la posición correcta
        if shift[2] != ':' or len(shift) != 5:
            return False

        return True

    @staticmethod
    def update_list_from_shift_start(pya_tuple_ordered, shift_start_in_timestamp_miliseconds):
        """
        Metodo que recibe una lista de tuplas de pya ordenadas, además de un tiempo de inicio de turno. Retorna
        la misma lista actualizada donde solo estén almacenados los datos a partir de la hora de inicio de turno.

        Parámetros:
        - pya_tuple_ordered: una lista de tuplas de pya ordenadas
        - shift_start: una hora de inicio de turno en timestamp milisegundos

        Return:
        - pya_tuple_ordered: la tupla actualizada a partir de la hora de inicio de turno
        """
        for i, t in enumerate(pya_tuple_ordered):
            if t[1] >= shift_start_in_timestamp_miliseconds:
                pya_tuple_ordered = pya_tuple_ordered[i:]
                break
        return pya_tuple_ordered

    @staticmethod
    def convert_to_pya_tuple(values_tuple):
        """
        Método que recibe una tupla de tuplas de ppm y las convierte a una tuple de pya. Esto lo utilizamos en los
        casos donde hay que utilizar los valores de ppm diario como valores de run-stop

        Parámetros:
        - values_tuple: una tupla de valores (generalmente será de ppm)

        Return:
        - values_tuple: esa lista de valores convertidas a valores de 0 y 1
        """
        for i in values_tuple:
            if i[0] > 1:
                values_tuple[values_tuple.index(i)] = (1, i[1])

        return values_tuple
