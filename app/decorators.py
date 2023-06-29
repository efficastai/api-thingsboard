import time


def mide_tiempo(funcion):
    def funcion_medida(*args, **kwargs):
        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        tiempo_ejecucion = time.time() - inicio
        print(f"Tiempo de ejecución de {funcion.__name__}: {tiempo_ejecucion} segundos")
        return resultado

    return funcion_medida
