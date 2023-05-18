import threading

from .PostgresQuery import *
from datetime import datetime


class CustomCalculation:
    """
    Clase CustomCalculation: Esta clase fue creada con el proposito de brindar calculos especificos principalmente
    para las maquinas de Tensar. Las estaciones, hormigoneras y desmoldes, producen datos que deben ser filtrados. Para
    esto, se crea una nueva tabla en la base de datos de Thingsobard que funciona para administrar las cuentas y los
    acumuladores de esas maquinas en particular, y asi obtener tablas ordenadas que son utilizadas en el front-end
    de la instancia Tensar. Además, requerimos conteos totales y parciales de ppm y pya, dependiendo el tipo de maquina,
    al ser un calculo puntual, también utilizamos esta clase para tratar ese tipo de máquina.
    """

    def __init__(self):
        self.query = PostgresQuery()
        self.date = datetime.now()
        self.flag = threading.Event()

    def get_tensar_custom_data(self, device, ts, value, interval=None, flag=None):
        """
        Método get_tensar_custom_data: Este método recibe un flag y un intervalo de manera opcional. En caso de
        recibirlo (el flag o el intervalo no son None), quiere decir que la maquina requiere un tratamiento especial
        en los datos. Para esto se irán haciendo distintos tipos de validaciones para comprobar si es necesario
        insertar datos en la tabla "tensar", y por consiguiente retornarlos hacia el front-end. En el caso
        que las validaciones sean falsas, el metodo no retorna datos para no alterar la vista de los ultimos datos
        que se ven en el front-end
        """
        flag = flag.lower() if flag is not None else None
        # Si el flag es de los puentes, retorno los acumulados de pya del dia y totales
        if flag == 'puente':
            pya_values = self.get_pya_values(device)
            return pya_values
        # Si el flag es de la caldera, retorno los acumulados de pya del dia y totales + el conteo diario de registros
        # de ppm
        if flag == 'caldera':
            pya_values = self.get_pya_values(device)
            ppm_count_values = self.get_ppm_count_day_accumulator(device)
            result = {**pya_values, **ppm_count_values}
            return result
        # Si el mensaje posee un intervalo, significa que pertenece al tipo de maquina que se le aplica un filtro
        # de tiempo entre mensajes. A partir de esto vienen validaciones (si el registro es de hoy, si existe o no y
        # si transcurrieron al menos 15 minutos entre ppm >= 1. Si no se cumplen las condiciones el metodo no retorna
        # nada
        if interval is not None:
            is_valid_value = value >= 1
            ts_int = int(ts)
            interval_to_milis = int(interval) * 60000
            if is_valid_value:
                insert_custom_data = self.insert_tensar_data(device, ts_int, interval_to_milis)
                if insert_custom_data:
                    last_register = self.get_tensar_last_register(device)
                    return last_register

        return None

    def insert_tensar_data(self, device, ts, interval):
        """
        Método insert_tensar_data: Este metodo recibe un dispositivo, un ts y un intervalo. Primero comprueba
        que existan registros del dispositivo en la tabla tensar, en caso de que no exista, ingresa el primer registro.
        Luego comprueba que el dato sea o no del mismo dia para empezar a contabilizar las piezas del dia. Por ultimo
        comprueba que exista una diferencia de tiempo entre valores positivos valida (esta diferencia se setea
        en el dispositivo en el que sea necesario utilizar el filtro de tiempo, utilizando el atributo de servidor
        "interval" y seteando en valor INTEGER el tiempo en minutos que necesitamos que pase entre medio).
        Si el dato no debe ser insertado porque no pasó las validaciones, el método retorna False.

        Parámetros:
        - device: un dispositivo
        - ts: la estampa de tiempo del dato
        - interval: el intervalo en minutos que sera aplicado como filtro

        Return:
        - False si no pasa las validaciones
        - True si el dato fue insertado con éxito
        """
        # Valores por defecto a insertar en el registro
        value = True
        dif = 0
        # Traigo el ultimo registro de timestamp, en caso de que no exista, es None
        try:
            last_ts = self.query.get_tensar_last_ts(device)[0][0]
        except IndexError:
            last_ts = None

        # Si no existe un ultimo registro, inserto el registro actual y retorno True
        if last_ts is None:
            self.query.insert_tensar_data(ts, value, dif, device)
            return True
        elif last_ts is not None:
            is_same_day = self.is_same_day(ts)
            # Si el registro no es del mismo dia, inserto el dato y retorno True
            if not is_same_day:
                self.query.insert_tensar_data(ts, value, dif, device)
                return True
            elif is_same_day:
                # Consulto si la diferencia es valida en la tabla general de Thingsboard
                valid_dif = self.is_valid_interval(ts, device, interval)
                # Si es una diferencia de tiempo valida, inserto el dato y retorno True
                if valid_dif is not False:
                    self.query.insert_tensar_data(ts, value, valid_dif, device)
                    return True

        return False

    def get_tensar_last_register(self, device):
        """
        Metodo que retorna un objeto JSON con los resultados obtenidos de la tabla de Tensar:
        ultimo ts y dif registrado, total acumulado de piezas del dia en base a los filtros que requieren ser
        aplicados.

        Parámetros:
        - device: un dispositivo


        Return:
        - Un objeto diccionario con la estampa de tiempo del dato, la diferencia, un ppm = 1, el acumulado del dia,
        de la semana, y del mes (esto en base al filtro necesario)
        """
        ppm = 1
        ts, dif = self.query.get_tensar_day_last_register(device)[0]
        day_accumulator = self.query.get_tensar_day_accumulator(device)[0][0]
        week_accumulator = self.query.get_tensar_week_accumulator(device)[0][0]
        month_accumulator = self.query.get_tensar_month_accumulator(device)[0][0]

        result = {
            'api_custom_tensar_ts': ts,
            'api_custom_tensar_dif': dif,
            'api_custom_tensar_ppm': ppm,
            'api_custom_tensar_day_accumulator': day_accumulator,
            'api_custom_tensar_week_accumulator': week_accumulator,
            'api_custom_tensar_month_accumulator': month_accumulator
        }

        return result

    def is_same_day(self, ts):
        """
        Metodo is_same_day: Este metodo compara un timestamp con la fecha actual, si coinciden ser del dia de hoy
        , retorna True, en caso contrario retorna False

        - Parámetros:
        - ts: una estampa de tiempo

        Return:
        - True si son del mismo dia
        - False en caso contrario
        """
        ts = ts / 1000
        ts_to_date = datetime.fromtimestamp(ts).date()
        if ts_to_date == self.date.date():
            return True

        return False

    def is_valid_interval(self, ts, device, interval):
        """
        Metodo is_valid_interval: Este metodo comprueba si existe una diferencia mayor o igual al numero en minutos
        seteados desde el dispositivo (atributo de dispositivos interval)

        Parámetros:
        - ts: la estampaa de tiempo del dato
        - device: el dispositivo
        - interval: el intervalo que fue seteado en los atributos del dispositivo

        Return:
        - False si no transucurrio el tiempo del intervalo
        - dif: la diferencia de tiempo entre el ultimo registro con tiempo valido y este.
        """
        last_ts = self.query.get_last_ts_where_ppm_equals_1(device)[0][0]
        dif = ts - last_ts
        if dif >= interval:
            return dif

        return False

    def get_pya_values(self, device):
        """
        Método get_pya_values: Este metodo retorna el acumulado de pya del dia y el acumulador historico de pya.
        Se utiliza principalmente para los puentes que desean saber las conmutaciones diarios y totoles.

        Parámetros:
        - device: un dispositivo

        Return:
        - Un objeto diccionario con los resultados de las querys.
        """
        pya_day_accumulator = int(self.query.get_pya_day_accumulator(device)[0][0])
        pya_total_accumulator = int(self.query.get_pya_total_accumulator(device)[0][0])
        result = {
            'api_day_pya_accumulator': pya_day_accumulator,
            'api_total_pya_accumulator': pya_total_accumulator
        }

        return result

    def get_ppm_count_day_accumulator(self, device):
        """
        Método get_ppm_count_day_accumulator: Este metodo cuenta la cantidad de registros de ppm que se registraron
        en el dia de hoy. Se utiliza principalmente para las maquinas del tipo caldera.

        Parámetros:
        - device: un dispositivo

        Return:
        - Un objeto diccionario con el conteo de registros de ppm del dia.
        """
        ppm_count_day_accumulator = int(self.query.get_ppm_count_day_accumulator(device)[0][0])

        result = {
            'api_custom_tensar_ppm_count_day_accumulator': ppm_count_day_accumulator
        }

        return result
