import json

from flask import request

from app import app
from .Settings import *
from .TimeCalculation import *
from .Accumulator import *


@app.route('/api/get_accumulators', methods=['POST'])
def get_accumulators():
    request_data = request.get_json()
    device = request_data['device']
    accumulator = Accumulator()
    machine_accumulators = accumulator.get_accumulators(device)
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
    setting = Settings()
    setting.run_setting(ppm)
    return setting, 200


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
    time_calculation = TimeCalculation()
    machine_time_calculations = time_calculation.get_machine_time_calculations(device_name, shift_start)
    return machine_time_calculations, 200
