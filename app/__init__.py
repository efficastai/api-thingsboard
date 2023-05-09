import ujson as json
from flask.json import JSONEncoder
from flask import Flask


# Cambiando encoder y decoder por defecto
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return json.dumps(obj)
        except TypeError:
            return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

from app import endpoints
