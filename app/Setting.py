class Setting:

    def __init__(self):
        pass

    @staticmethod
    def run_setting(ppm):
        """
        Método que convierte run en 1 si el ppm es mayor a 0. Este metodo se utiliza para medir el encendido, apagado
        de ciertas soldadoras en base a su valor de ppm.
        @params: ppm
        @return: json run:valor_de_run
        """
        run = 1 if ppm > 0 else 0
        return {'api_run': run}

    @staticmethod
    def fix_values(values_list, fix):
        """
        Método que recibe una lista de valores que convertir y una bandera que indica qué tipo de conversión realizar.
        Por el momento utilizamos:
         - s10 para describir soldadoras que haya que ajustar / 10 sus valores
         - s20 para describir soldadoras que haya que ajustar / 20 sus valores

        Parámetros:
        - values_list: Una lista o tupla de valores o un valor individual
        - fix: Un valor que describe el ajuste que hay que realizar

        Return:
        - fixed_values_list: la lista de los valores ajustados
        """
        fixed_values_list = []
        fix = float(fix)

        if isinstance(values_list, (list, tuple)):  # Verificar si es una lista o tupla de valores
            for i in values_list:
                if i == 0:
                    fixed_values_list.append(i)
                    continue
                fixed_values_list.append(round(i * fix))
        else:  # Si es un solo valor entero
            if values_list != 0:
                fixed_values_list = [round(values_list * fix)]
            else:
                return 0

        return fixed_values_list

