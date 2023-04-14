import pytest
import requests

ENDPOINT = "http://127.0.0.1:5000"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_imprimir_acumulador():
    # Definir los datos de prueba
    data = {'device': 'EXXBA'}

    # Enviar una solicitud POST al endpoint
    response = requests.post('http://66.97.37.100/api/imprimir_acumulador', json=data)

    # Comprobar si la respuesta es correcta
    assert response.status_code == 200
    assert isinstance(response.json()['acumulador_prueba'], float) and response.json()['acumulador_prueba'] > 0
