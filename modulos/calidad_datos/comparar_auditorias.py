import csv


def leer_historial(ruta):

    with open(
        ruta,
        "r",
        encoding="utf-8-sig"
    ) as archivo:

        lector = csv.DictReader(archivo)

        auditorias = list(lector)

    return auditorias


def comparar_ultimas_auditorias(ruta):

    auditorias = leer_historial(ruta)

    if len(auditorias) < 2:
        return {
            "estado": "INSUFICIENTES",
            "mensaje": "Se necesitan al menos dos auditorías para realizar una comparación."
        }

    anterior = auditorias[-2]
    actual = auditorias[-1]

    diferencia_alertas = (
        int(actual["errores"]) +
        int(actual["advertencias"])
    ) - (
        int(anterior["errores"]) +
        int(anterior["advertencias"])
    )

    diferencia_afectados = (
        int(actual["registros_afectados"])
        -
        int(anterior["registros_afectados"])
    )

    diferencia_sin_alertas = (
        int(actual["registros_sin_alertas"])
        -
        int(anterior["registros_sin_alertas"])
    )

    diferencia_porcentaje = (
        float(actual["porcentaje_sin_alertas"])
        -
        float(anterior["porcentaje_sin_alertas"])
    )

    return {
        "estado": "OK",
        "anterior": anterior,
        "actual": actual,
        "diferencia_alertas": diferencia_alertas,
        "diferencia_afectados": diferencia_afectados,
        "diferencia_sin_alertas": diferencia_sin_alertas,
        "diferencia_porcentaje": diferencia_porcentaje
    }