import csv
import os


def exportar_errores_csv(errores, ruta_salida):
    os.makedirs(
        os.path.dirname(ruta_salida),
        exist_ok=True
    )

    columnas = [
        "registro",
        "regla",
        "nivel",
        "campo",
        "subcampo",
        "problema",
        "sugerencia"
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

        for error in errores:
            escritor.writerow(error)