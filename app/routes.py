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
    pya = request_data['pya']
    ppm = request_data['ppm']
    timestamp = datetime.fromtimestamp(request_data['ss_lastActivityTime'] / 1000).strftime("%d/%m/%Y - %H:%M:%S")
    return json.dumps({'sumando': pya + ppm,
                       'datatime': timestamp}), 200
