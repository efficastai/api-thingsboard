import json
from app import app
from .TsKvQuery import *
from .Calculations import *
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


@app.route('/api/get_accumulator', methods=['POST'])
def get_accumulator():
    request_data = request.get_json()
    device = request_data['device']
    new_query = TsKvQuery()
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
    run_soldadoras = 0
    if ppm2 > 0:
        run_soldadoras = 1
    return json.dumps({'run_soldadoras': run_soldadoras}, default=int), 200


@app.route('/api/test_delta', methods=['POST'])
def test_delta():
    request_data = request.get_json()
    device = request_data['device']
    new_query = TsKvQuery()
    api_all_pya = new_query.get_all_pya_values(device)
    new_calculation = Calculations()
    api_ratio_shift_time = new_calculation.calculate_time_values(api_all_pya)
    print(api_ratio_shift_time)
    return json.dumps({'ratio_shift_time_test': api_ratio_shift_time})


