import json
from app import app, TsKvQuery
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


@app.route('/api/imprimir_acumulador', methods=['POST'])
def imprimir_acumulador():
    new_query = TsKvQuery.TsKvQuery
    request_data = request.get_json()
    if request_data:
        if 'PPM2' in request_data:
            acumulador_de_prueba_diario = new_query.acumulador_ppm_diario()
    return json.dumps({'acumulador_de_prueba_diario': acumulador_de_prueba_diario})


