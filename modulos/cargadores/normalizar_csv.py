import csv

from modulos.cargadores.analizar_csv import (
    analizar_csv
)

from modulos.cargadores.mapear_columnas import (
    mapear_columna
)


CAMPOS_ESTANDAR = [
    "001",
    "titulo",
    "autor",
    "isbn",
    "editorial",
    "anio",
    "ubicacion",
    "codigo_barras",
    "tipo_material"
]


def normalizar_catalogo_csv(ruta):

    analisis = analizar_csv(
        ruta
    )

    separador = analisis["separador"]

    columnas_originales = (
        analisis["columnas"]
    )

    mapeo = {}
    columnas_desconocidas = []

    for columna in columnas_originales:

        campo_estandar = mapear_columna(
            columna
        )

        if campo_estandar:

            mapeo[columna] = campo_estandar

        else:

            columnas_desconocidas.append(
                columna
            )

    catalogo = []

    with open(
        ruta,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        lector = csv.DictReader(
            archivo,
            delimiter=separador
        )

        for fila in lector:

            registro = {}

            for campo in CAMPOS_ESTANDAR:

                registro[campo] = ""

            for columna_original, campo_estandar in mapeo.items():

                registro[campo_estandar] = (
                    fila.get(
                        columna_original,
                        ""
                    ).strip()
                )

            catalogo.append(
                registro
            )

    return {
        "catalogo": catalogo,
        "mapeo": mapeo,
        "columnas_originales": columnas_originales,
        "columnas_desconocidas": columnas_desconocidas
    }