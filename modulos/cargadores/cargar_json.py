import json


def cargar_catalogo_json(ruta):
    with open(
        ruta,
        "r",
        encoding="utf-8"
    ) as archivo:

        catalogo = json.load(archivo)

    return catalogo