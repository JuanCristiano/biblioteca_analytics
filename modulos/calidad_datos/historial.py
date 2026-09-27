import csv
import os
from datetime import datetime


def generar_id_auditoria():

    return datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


def crear_directorio_auditoria(id_auditoria):

    ruta = os.path.join(
        "data",
        "historial",
        id_auditoria
    )

    os.makedirs(
        ruta,
        exist_ok=True
    )

    return ruta


def guardar_auditoria(resumen, ruta_salida):

    os.makedirs(
        os.path.dirname(ruta_salida),
        exist_ok=True
    )

    columnas = [
        "fecha",
        "registros",
        "registros_afectados",
        "registros_sin_alertas",
        "porcentaje_sin_alertas",
        "errores",
        "advertencias"
    ]

    existe_archivo = os.path.exists(
        ruta_salida
    )

    with open(
        ruta_salida,
        "a",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas
        )

        if not existe_archivo:
            escritor.writeheader()

        escritor.writerow({
            "fecha": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "registros": resumen["total_registros"],
            "registros_afectados": resumen[
                "registros_afectados"
            ],
            "registros_sin_alertas": resumen[
                "registros_sin_problemas"
            ],
            "porcentaje_sin_alertas": round(
                resumen["porcentaje_sin_problemas"],
                1
            ),
            "errores": resumen["errores"],
            "advertencias": resumen["advertencias"]
        })