import csv


def detectar_separador(ruta):
    with open(
        ruta,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        muestra = archivo.read(4096)

    dialecto = csv.Sniffer().sniff(
        muestra,
        delimiters=",;\t|"
    )

    return dialecto.delimiter


def detectar_columnas(ruta, separador):
    with open(
        ruta,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        lector = csv.reader(
            archivo,
            delimiter=separador
        )

        encabezados = next(lector)

    return encabezados


def analizar_csv(ruta):
    separador = detectar_separador(
        ruta
    )

    columnas = detectar_columnas(
        ruta,
        separador
    )

    return {
        "separador": separador,
        "columnas": columnas
    }