from flask import Flask
import ujson as json

app = Flask(__name__)
app.json_encoder = json.JSONEncoder
app.json_decoder = json.JSONDecoder

from app import endpoints
