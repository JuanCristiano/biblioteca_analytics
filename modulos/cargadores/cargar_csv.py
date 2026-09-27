import csv


def cargar_catalogo_csv(ruta):
    catalogo = []

    with open(
        ruta,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:
            catalogo.append(dict(fila))

    return catalogo