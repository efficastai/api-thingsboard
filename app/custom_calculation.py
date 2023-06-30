from .postgres_query_builder import *


class CustomCalculation:
    """
    Clase CustomCalculation: Esta clase proporciona cálculos específicos principalmente para las máquinas de Tensar.
    Las máquinas de las estaciones, hormigoneras y desmoldes producen datos que requieren filtrado. Para ello, se crea
    una nueva tabla en la base de datos de Thingsboard para administrar las cuentas y los acumuladores de estas máquinas
    en particular, y así obtener tablas ordenadas que se utilizan en el front-end de la instancia Tensar. Además, se
    necesitan conteos totales y parciales de ppm y pya, según el tipo de máquina. Esta clase también se utiliza para
    tratar cálculos puntuales específicos de ciertos tipos de máquinas.
    """

    def __init__(self):
        self.query = PostgreSQLQueryBuilder()
        self.date = datetime.now()

    def get_custom_data(self, device, ts, value, interval=None, flag=None, pya=None, daily_target=None):
        """
        Método get_tensar_custom_data: Este método recibe un flag y un intervalo de manera opcional. En caso de
        recibirlo (el flag o el intervalo no son None), quiere decir que la maquina requiere un tratamiento especial
        en los datos. Para esto se irán haciendo distintos tipos de validaciones para comprobar si es necesario
        insertar datos en la tabla "tensar", y por consiguiente retornarlos hacia el front-end. En el caso
        que las validaciones sean falsas, el metodo no retorna datos para no alterar la vista de los ultimos datos
        que se ven en el front-end

        Parámetros:

        Retorno:

        """
        flag = flag.lower() if flag is not None else None

        if flag == 'puente':
            return self._get_bridge_data(device, 6, ts, pya)
        elif flag == 'caldera':
            return self._get_caldera_data(device)
        elif interval is not None:
            return self._process_interval_data(device, ts, value, interval, daily_target)

        return None

    def _get_bridge_data(self, device, inactivity_interval, ts, pya):
        """
        Comentarios del metodo
        """
        pya_values = self.get_pya_values(device)
        check_machine_inactivity = self.check_machine_inactivity(device, inactivity_interval, pya, ts)
        if check_machine_inactivity is None:
            return pya_values
        result = {**pya_values, **check_machine_inactivity}
        return result

    def _get_caldera_data(self, device):
        """
        Comentarios del metodo
        """
        pya_values = self.get_pya_values(device)
        ppm_count_values = self.get_ppm_count_day_accumulator(device)
        result = {**pya_values, **ppm_count_values}
        return result

    def _process_interval_data(self, device, ts, value, interval, daily_target):
        """
        Comentarios del método

        Parámetros:
        - device
        - ts
        - value
        - interval

        Retorno:

        """
        is_valid_value = value >= 1
        ts_int = int(ts)
        interval_to_milis = int(interval) * 60000
        if is_valid_value:
            insert_custom_data = self.insert_tensar_data(device, ts_int, interval_to_milis)
            if insert_custom_data:
                last_register = self.get_tensar_last_register(device, daily_target)
                return last_register

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
        counter = 1
        # Traigo el ultimo registro de timestamp, en caso de que no exista, es None
        try:
            last_ts = self.query.get_tensar_last_ts(device)[0][0]
        except IndexError:
            last_ts = None

        # Si no existe un ultimo registro, inserto el registro actual y retorno True
        if last_ts is None:
            self.query.insert_tensar_data(ts, value, dif, device, counter)
            return True
        elif last_ts is not None:
            is_same_day = self.is_same_day(last_ts)
            # Si el registro no es del mismo dia, inserto el dato y retorno True
            if not is_same_day:
                self.query.insert_tensar_data(ts, value, dif, device, counter)
                return True
            elif is_same_day:
                # Consulto si la diferencia es valida en la tabla general de Thingsboard
                valid_dif = self.is_valid_interval(ts, device, interval)
                # Si es una diferencia de tiempo valida, inserto el dato y retorno True
                if valid_dif:
                    self.query.insert_tensar_data(ts, value, valid_dif, device, 0)
                    return True

        return False

    def get_tensar_last_register(self, device, daily_target):
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
        daily_compliance_percentege = self.get_custom_daily_compliance_percentege(day_accumulator, daily_target)

        result = {
            'api_custom_tensar_ts': ts,
            'api_custom_tensar_dif': dif,
            'api_custom_tensar_ppm': ppm,
            'api_custom_tensar_day_accumulator': day_accumulator,
            'api_custom_tensar_week_accumulator': week_accumulator,
            'api_custom_tensar_month_accumulator': month_accumulator,
            'api_custom_tensar_daily_compliance_percentege': daily_compliance_percentege
        }

        return result

    @staticmethod
    def get_custom_daily_compliance_percentege(day_accumulator, daily_target):
        """
        Comentarios del metodo
        """
        daily_compliance_percentege = round(day_accumulator * 100 / daily_target) if daily_target is not None else 'Set'

        return daily_compliance_percentege

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
        try:
            pya_day_accumulator = int(self.query.get_pya_day_accumulator(device)[0][0])
        except Exception as e:
            pya_day_accumulator = 0
            print("Exception en Custom Calculation, get_pya_values", e)
        try:
            pya_total_accumulator = int(self.query.get_pya_total_accumulator(device)[0][0])
        except Exception as e:
            pya_total_accumulator = 0
            print("Exception en Custom Calculation, get_pya_values", e)
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

    def check_machine_inactivity(self, device, inactivity_interval, pya, ts):
        """
        Comentarios del metodo
        """
        if pya == 0:
            return self._case_pya_0(device, inactivity_interval)

        elif pya == 1:
            return self._case_pya_1(device, ts)

        return None

    def _case_pya_0(self, device, inactivity_interval):
        """
        Comentarios del método

        @params
        """
        sum_last_n_pya = int(self.query.get_pya_last_n_values(device, inactivity_interval)[0][0])
        if sum_last_n_pya == 0:
            try:
                last_ts, last_value = self.query.get_tensar_day_last_value(device)[0]
            except IndexError:
                last_value = None
            if last_value is None or last_value:
                counter = 1
                first_stop_ts = self.query.get_pya_last_n_registers_asc(device, inactivity_interval)[0][0]
                if last_value is not None:
                    counter = int(self.query.get_tensar_last_counter(device)[0][0])
                    counter += 1

                self.query.insert_tensar_data(first_stop_ts, False, 0, device, counter)
                result = {
                    "api_custom_tensar_stop_ts": first_stop_ts,
                    "api_custom_tensar_stop_counter": counter,
                    "api_custom_tensar_stop_dif": 0
                }
                return result

        return None

    def _case_pya_1(self, device, ts):
        """
        Comentarios del metodo

        Parametros:

        Retorno:

        """
        try:
            last_ts, last_value = self.query.get_tensar_day_last_value(device)[0]
        except Exception as e:
            print("Exception en _case_pya_1", e)
            last_value = None
            last_ts = None

        if last_value is not None and not last_value:
            ts = int(ts)
            dif = ts - last_ts
            self.query.update_tensar_last_value(True, dif, device)

            result = {
                "api_custom_tensar_stop_dif": dif,
                "api_custom_tensar_stop_last_ts": last_ts
            }

            return result

        return None
