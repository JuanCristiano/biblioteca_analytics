
import csv


def cargar_fuente_autores(ruta):
    """
    Carga una fuente externa de autores desde un archivo CSV.

    El CSV debe contener:

        001,autor

    El campo 001 identifica el registro del catálogo.
    El campo autor contiene el/los autores de la fuente externa.

    Devuelve un diccionario:

        {
            "000001": "Borges, Jorge Luis",
            "000002": "Cortázar, Julio",
            ...
        }

    No modifica los datos originales.
    """

    fuente = {}

    with open(
        ruta,
        "r",
        encoding="utf-8",
        newline=""
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            identificador = (
                fila.get("001", "")
                or ""
            ).strip()

            autor = (
                fila.get("autor", "")
                or ""
            ).strip()

            if not identificador:
                continue

            fuente[identificador] = autor

    return fuente
