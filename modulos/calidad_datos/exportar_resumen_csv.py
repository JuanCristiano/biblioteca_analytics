import csv
import os


def exportar_resumen_csv(indicadores, ruta_salida):
    os.makedirs(
        os.path.dirname(ruta_salida),
        exist_ok=True
    )

    columnas = [
        "regla",
        "registros_afectados",
        "porcentaje_afectados",
        "cantidad_problemas"
    ]

    with open(
        ruta_salida,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas
        )

        escritor.writeheader()

        for regla, datos in indicadores.items():
            escritor.writerow({
                "regla": regla,
                "registros_afectados": datos["registros_afectados"],
                "porcentaje_afectados": round(
                    datos["porcentaje"],
                    1
                ),
                "cantidad_problemas": datos["problemas"]
            })