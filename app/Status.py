import time

from .PostgresQuery import *


class Status:

    def __init__(self):
        self.query = PostgresQuery()

    def get_machine_status(self, client, device, status, flag=None):
        """
        Método que devuelve la cantidad de máquinas encendidas, apagadas y totales por empresa, consultando a una
        tabla que actualiza sus registros en base al cambio de estado. En caso de que la maquina se reporte por
        primera vez, los métodos insertan el registro y luego comienzan a actualizarlo. El calculo se realiza por
        cada entrada de pya a la API.

        Parámetros:
        - client: un cliente
        - device: un dispositivo
        - status: el estado de la maquina

        Return:
        - Un objeto JSON con la información del status de todas las máquinas del cliente en cuestión
        """
        # Identifico si el dispositivo tiene un flag nodo, en ese caso elimino el registro de dicho dispositivo,
        # ya que por el momento no interesa contar si esta encendido o no.
        flag = flag.lower() if flag is not None else None
        if flag == 'nodo':
            self.query.delete_node_device(device)
            print("Hubo un DELETE!")

        self.insert_machine_status(client, device, status)
        machines_on, machines_off, total_machines = self.get_total_on_off(client)

        return {
            'api_machines_on': machines_on,
            'api_machines_off': machines_off,
            'api_total_machines': total_machines
        }

    def insert_machine_status(self, client, device, status):
        """
        Método que inserta el estado de la máquina en una tabla de la base de datos de Thingsboard llamada machines.
        Esta tabla cuenta con id, client, device, status. Se utiliza para actualizar el estado actual de la maquina
        y así verificar cuantas maquinas se encuentran encendidas y cuantas apagadas.

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
