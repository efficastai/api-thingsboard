class Settings:

    def __init__(self):
        pass

    @staticmethod
    def run_setting(ppm):
        """
        Método que convierte run en 1 si el ppm es mayor a 0. Este metodo se utiliza para medir el encendido, apagado
        de ciertas soldadoras en base a su valor de ppm
        @params: ppm
        @return: json run:valor_de_run
        """
        run = 1 if ppm > 0 else 0
        return {'api_setting_run': run}
