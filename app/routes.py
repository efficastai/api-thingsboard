import json
from app import app
from .Query import *
from .TimeCalculation import *
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


@app.route('/api/run_soldadoras', methods=['POST'])
def run_soldadoras():
    request_data = request.get_json()
    ppm2 = request_data['PPM2']
    run = 0
    if ppm2 > 0:
        run = 1
    return json.dumps({'run_soldadoras': run}, default=int), 200


@app.route('/api/time_calculations', methods=['POST'])
def time_calculations():
    request_data = request.get_json()
    device = request_data['device']
    shift_start = None
    if 'shift_start' in request_data:
        shift_start = request_data['shift_start']
    time_calculation = TimeCalculation()
    api_machine_time_calculations = time_calculation.get_machine_time_calculations(device, shift_start)
    return json.dumps(api_machine_time_calculations)
