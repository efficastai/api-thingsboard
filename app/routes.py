import json
from app import app
from flask import request
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return 'Hello'


@app.route('/api/prueba', methods=['POST'])
def receive_parameters():
    request_data = request.get_json()
    ppm = None
    if request_data:
        if 'PPM2' in request_data:
            ppm = request_data['PPM2']
        timestamp = datetime.fromtimestamp(request_data['ss_lastActivityTime'] / 1000).strftime("%d/%m/%Y - %H:%M:%S")
    return json.dumps({'ajuste_ppm_prueba': ppm * 0.5,
                       'datatime': timestamp}), 200
