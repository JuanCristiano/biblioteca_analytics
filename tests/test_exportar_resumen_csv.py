import csv

from modulos.calidad_datos.exportar_resumen_csv import exportar_resumen_csv

COLUMNAS = [
    "regla", "registros_afectados",
    "porcentaje_afectados", "cantidad_problemas",
]


def leer_csv(ruta):
    with open(ruta, "r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return lector.fieldnames, list(lector)


def test_escribe_una_fila_por_regla(tmp_path):
    ruta = tmp_path / "resumen.csv"
    indicadores = {
        "REGLA-001": {"registros_afectados": 1, "porcentaje": 10.0, "problemas": 1},
        "REGLA-002": {"registros_afectados": 2, "porcentaje": 20.0, "problemas": 3},
    }

    exportar_resumen_csv(indicadores, str(ruta))

    columnas, filas = leer_csv(ruta)
    assert columnas == COLUMNAS
    assert len(filas) == 2
    assert filas[0] == {
        "regla": "REGLA-001",
        "registros_afectados": "1",
        "porcentaje_afectados": "10.0",
        "cantidad_problemas": "1",
    }
    assert filas[1]["regla"] == "REGLA-002"
    assert filas[1]["cantidad_problemas"] == "3"


def test_redondea_el_porcentaje_a_un_decimal(tmp_path):
    ruta = tmp_path / "resumen.csv"
    indicadores = {
        "REGLA-001": {"registros_afectados": 1, "porcentaje": 33.3333, "problemas": 1},
    }

    exportar_resumen_csv(indicadores, str(ruta))

    _, filas = leer_csv(ruta)
    assert filas[0]["porcentaje_afectados"] == "33.3"


def test_crea_las_carpetas_que_no_existen(tmp_path):
    ruta = tmp_path / "processed" / "exportaciones" / "resumen.csv"

    exportar_resumen_csv({}, str(ruta))

    assert ruta.exists()


def test_sin_indicadores_genera_solo_el_encabezado(tmp_path):
    ruta = tmp_path / "resumen.csv"

    exportar_resumen_csv({}, str(ruta))

    columnas, filas = leer_csv(ruta)
    assert columnas == COLUMNAS
    assert filas == []