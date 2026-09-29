import csv

from modulos.calidad_datos.exportar_csv import exportar_errores_csv

COLUMNAS = [
    "registro", "regla", "nivel", "campo",
    "subcampo", "problema", "sugerencia",
]


def error_ejemplo(registro="000008", problema="Título principal vacío"):
    return {
        "registro": registro,
        "regla": "REGLA-001",
        "nivel": "ERROR",
        "campo": "245",
        "subcampo": "a",
        "problema": problema,
        "sugerencia": "Revisar y completar 245$a.",
    }


def leer_csv(ruta):
    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return lector.fieldnames, list(lector)


def test_escribe_encabezado_y_una_fila_por_problema(tmp_path):
    ruta = tmp_path / "salida.csv"
    errores = [error_ejemplo("000008"), error_ejemplo("000009")]

    exportar_errores_csv(errores, str(ruta))

    columnas, filas = leer_csv(ruta)
    assert columnas == COLUMNAS
    assert len(filas) == 2
    assert filas[0]["registro"] == "000008"
    assert filas[0]["regla"] == "REGLA-001"
    assert filas[0]["nivel"] == "ERROR"
    assert filas[1]["registro"] == "000009"


def test_crea_las_carpetas_que_no_existen(tmp_path):
    ruta = tmp_path / "processed" / "auditorias" / "salida.csv"

    exportar_errores_csv([error_ejemplo()], str(ruta))

    assert ruta.exists()


def test_lista_vacia_genera_solo_el_encabezado(tmp_path):
    ruta = tmp_path / "salida.csv"

    exportar_errores_csv([], str(ruta))

    columnas, filas = leer_csv(ruta)
    assert columnas == COLUMNAS
    assert filas == []


def test_conserva_tildes_y_usa_bom_para_excel(tmp_path):
    ruta = tmp_path / "salida.csv"

    exportar_errores_csv([error_ejemplo(problema="Título principal vacío")], str(ruta))

    assert ruta.read_bytes().startswith(b"\xef\xbb\xbf")
    _, filas = leer_csv(ruta)
    assert filas[0]["problema"] == "Título principal vacío"