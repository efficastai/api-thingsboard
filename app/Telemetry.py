import time
from random import randint

import paho.mqtt.client as mqtt


class Telemetry:

    def __init__(self):
        self.broker = '200.58.106.167'
        self.port = 1883

    def on_connect(client, userdata, flags, rc):
        print("Connection OK" if rc == 0 else print("Connection FAIL"))

    # LOG de conexion
    def on_log(client, userdata, level, buf):
        print("Log: " + buf)

    # Metodo para publicar mensajes
    def on_publish(client, userdata, result):
        print("Data publicada a Thingsboard")

    # Respuesta cuando recibimos un PUBLISH del servidor
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def send_telemetry(self, access_token, device_status):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_log = self.on_log
        client.on_publish = self.on_publish
        client.on_message = self.on_message
        client.username_pw_set(access_token)
        client.connect(self.broker, self.port, keepalive=60)
        client.loop_start()

        while True:
            pya = randint(0, 1)
            ppm = randint(0, 40)
            payload = "{"
            payload += "\"ANDA\":" + str(ppm) + ","
            payload += "\"ANDA2\":" + str(pya)
            payload += "}"
            client.publish("v1/devices/me/telemetry", payload)
            print(payload)
            time.sleep(20)
