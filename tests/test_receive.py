import pytest
import requests

ENDPOINT = "http://127.0.0.1:5000"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_receive_parameters():
    payload = {
        "pya": 100,
        "ppm": 50
    }
    response = requests.post(ENDPOINT + "/receiveParameters", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data['sumando'] == 150
    print(data)
