from flask import request

from app import app
from .ProductionTracking import *
from .Setting import *
from .TimeCalculation import *


@app.route('/api/production_tracking_analysis', methods=['POST'])
def production_tracking_analysis():
    """
        Retorna un objeto JSON con variables de acumuladores. Por el momento: diario, semanal, mensual y ultimos
        10 valores. Tener en cuenta que ciertos valores dependiendo del flag se encuentran ajustados (caso
        soldadoras)

        Parámetros esperados en el body de la solicitud:
        - device: un dispositivo
        - flag (opcional): un flag para realizar un ajuste sobre los valores
        - target (opcional): el numero de piezas esperadas del dia
        - cycle_time (opcional): el numero de piezas esperadas por hora

        Retorno:
        - Un objeto JSON con los valores de los acumuladores
    """
    request_data = request.get_json()
    device = request_data.get('device')
    flag = request_data.get('flag')
    daily_target = request_data.get('daily_target')
    cycle_time = request_data.get('cycle_time')
    production_traking = ProductionTracking()
    machine_accumulators = production_traking.get_production_tracking_analysis(device, flag, daily_target, cycle_time)
    return machine_accumulators, 200


@app.route('/api/settings', methods=['POST'])
def settings():
    """
        Retorna un objeto JSON con ajustes para una máquina específica.

        Parámetros esperados en el body de la solicitud:

        Retorno:
        - Un objeto JSON con los ajustes para la máquina especificada.
        """
    request_data = request.get_json()
    ppm = request_data.get('PPM2')
    setting = Setting()
    run_but_ppm = setting.run_setting(ppm)
    return run_but_ppm, 200


@app.route('/api/time_calculations', methods=['POST'])
def time_calculations():
    """
    Retorna un objeto JSON con cálculos de tiempo para una máquina específica.

    Parámetros esperados en el body de la solicitud:
    - device: el nombre del dispositivo
    - shift_start (opcional): la hora de inicio del turno

    Retorno:
    - Un objeto JSON con los cálculos de tiempo para la máquina especificada.
    """
    request_data = request.get_json()
    device_name = request_data.get('device')
    shift_start = request_data.get('shift_start')
    flag = request_data.get('flag')
    time_calculation = TimeCalculation()
    machine_time_calculations = time_calculation.get_machine_time_calculations(device_name, shift_start, flag)
    return machine_time_calculations, 200
