import time

from .PostgresQuery import *


class Status:

    def __init__(self):
        self.query = PostgresQuery()

    def get_machine_status(self, client, device, status):
        self.insert_machine_status(client, device, status)
        machines_on, machines_off, total_machines = self.get_total_on_off(client)

        return {
            'api_machines_on': machines_on,
            'api_machines_off': machines_off,
            'api_total_machines': total_machines
        }

    def insert_machine_status(self, client, device, status):
        """
        Método que inserta el estado de la máquina en una base de datos SQLITE de estructura simple.
        Por el momento la base de datos se utiliza unicamente para esa funcion.

        Parámetros:
        - client: un clinete
        - device: un dispositivo
        - machine_state: el estado de la maquina (pya)
        """
        try:
            last_status = self.query.get_last_status(device)[0][0]
        except IndexError:
            last_status = None
            print("Estoy en el except. LAST STATUS: ", last_status)

        if last_status != status or last_status is None:
            self.query.insert_state(client, device, status)

    def get_total_on_off(self, client):
        """
        Método que obtiene la cantidad de maquinas encendidas, la cantidad de maquinas apagadas y la cantidad
        total de maquinas por cliente. Esto sucede cada vez que una maquina reporta un pya, ya que en ese momento
        se actualiza el estado de la maquina, por lo cual este metodo devuelve en tiempo real los resultados.

        Parámetros:
        - client: un cliente
        """
        time.sleep(2)
        machines_on = self.query.count_machines_on(client)[0][0]
        total_machines = self.query.count_total_machines(client)[0][0]
        machines_off = total_machines - machines_on

        return machines_on, machines_off, total_machines
