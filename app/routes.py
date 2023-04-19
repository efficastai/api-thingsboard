import json
from app import app
from .Query import *
from .TimeCalculation import *
from .Settings import *
from flask import request
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return 'Hello'


@app.route('/api/prueba', methods=['POST'])
def receive_parameters():
    request_data = request.get_json()
    pp10s = None
    timestamp = None
    if request_data:
        if 'PP10S' in request_data:
            pp10s = request_data['PP10S']
        if 'ss_lastActivityTime' in request_data:
            timestamp = datetime.fromtimestamp(request_data['ss_lastActivityTime'] / 1000).strftime("%d/%m/%Y - "
                                                                                                    "%H:%M:%S")
    return json.dumps({'ajuste_ppm_prueba': pp10s * 0.5,
                       'datatime': timestamp}), 200


@app.route('/api/get_accumulators', methods=['POST'])
def get_accumulators():
    request_data = request.get_json()
    device = request_data['device']
    new_query = Query()
    api_today_accumulator = new_query.get_today_accumulator(device=device)[0][0]
    api_week_accumulator = new_query.get_week_accumulator(device=device)[0][0]
    api_month_accumulator = new_query.get_month_accumulator(device=device)[0][0]
    api_last_ten_values = new_query.get_last_n_values(device=device, n=10)[0][0]
    return json.dumps({'api_today_accumulator': api_today_accumulator,
                       'api_week_accumulator': api_week_accumulator,
                       'api_month_accumulator': api_month_accumulator,
                       'api_last_ten_values': api_last_ten_values}, default=float), 200


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
    setting = Settings()
    setting.run_setting(ppm)
    return setting, 200


@app.route('/api/time_calculations', methods=['POST'])
def time_calculations():
    """
    Retorna un objeto JSON con cálculos de tiempo para una máquina específica.

    Parámetros esperados en el body de la solicitud:
    - device: el nombre de la máquina
    - shift_start (opcional): la hora de inicio del turno

    Retorno:
    - Un objeto JSON con los cálculos de tiempo para la máquina especificada.
    """
    request_data = request.get_json()
    device_name = request_data.get('device')
    shift_start = request_data.get('shift_start')
    time_calculation = TimeCalculation()
    machine_time_calculations = time_calculation.get_machine_time_calculations(device_name, shift_start)
    return machine_time_calculations, 200
