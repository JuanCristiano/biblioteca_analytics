import csv

import pytest

from modulos.cargadores.analizar_csv import (
    analizar_csv,
    detectar_columnas,
    detectar_separador,
)

SEPARADORES = [",", ";", "\t", "|"]

COLUMNAS = ["001", "titulo", "autor", "isbn"]

FILAS = [
    COLUMNAS,
    ["1", "Rayuela", "Julio Cortázar", "9780000000001"],
    ["2", "El Aleph", "Jorge Luis Borges", "9780000000002"],
    ["3", "Ficciones", "Jorge Luis Borges", "9780000000003"],
]


def crear_csv(tmp_path, separador, filas=FILAS, encoding="utf-8"):
    ruta = tmp_path / "datos.csv"
    contenido = "".join(separador.join(fila) + "\n" for fila in filas)
    ruta.write_text(contenido, encoding=encoding)
    return ruta


# ---------- detectar_separador ----------

@pytest.mark.parametrize("separador", SEPARADORES)
def test_detecta_el_separador(tmp_path, separador):
    ruta = crear_csv(tmp_path, separador)

    assert detectar_separador(ruta) == separador


def test_detecta_el_separador_en_un_archivo_con_bom(tmp_path):
    ruta = crear_csv(tmp_path, ";", encoding="utf-8-sig")

    assert detectar_separador(ruta) == ";"


# ---------- detectar_columnas ----------

@pytest.mark.parametrize("separador", SEPARADORES)
def test_lee_los_encabezados(tmp_path, separador):
    ruta = crear_csv(tmp_path, separador)

    assert detectar_columnas(ruta, separador) == COLUMNAS


def test_el_bom_no_se_pega_al_primer_encabezado(tmp_path):
    ruta = crear_csv(tmp_path, ",", encoding="utf-8-sig")

    assert detectar_columnas(ruta, ",")[0] == "001"


def test_un_encabezado_entre_comillas_puede_contener_el_separador(tmp_path):
    ruta = tmp_path / "comillas.csv"
    ruta.write_text('"Título, principal",autor\nRayuela,Cortázar\n', encoding="utf-8")

    assert detectar_columnas(ruta, ",") == ["Título, principal", "autor"]


def test_conserva_tildes_mayusculas_y_espacios_internos(tmp_path):
    ruta = crear_csv(
        tmp_path, ";",
        filas=[["Título Principal", "Año publicación"], ["a", "b"]],
    )

    assert detectar_columnas(ruta, ";") == ["Título Principal", "Año publicación"]


# ---------- analizar_csv ----------

@pytest.mark.parametrize("separador", SEPARADORES)
def test_analizar_csv_devuelve_separador_y_columnas(tmp_path, separador):
    ruta = crear_csv(tmp_path, separador)

    assert analizar_csv(ruta) == {"separador": separador, "columnas": COLUMNAS}


def test_analizar_csv_acepta_la_ruta_como_texto(tmp_path):
    ruta = crear_csv(tmp_path, ",")

    assert analizar_csv(str(ruta))["separador"] == ","


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

def test_limitacion_los_encabezados_no_se_limpian(tmp_path):
    ruta = crear_csv(
        tmp_path, ";",
        filas=[["001", " titulo ", "autor"], ["1", "a", "b"], ["2", "c", "d"]],
    )

    assert detectar_columnas(ruta, ";") == ["001", " titulo ", "autor"]


def test_limitacion_un_archivo_guardado_como_ansi_no_se_puede_leer(tmp_path):
    # Es lo que produce el "CSV (delimitado por comas)" de Excel en español.
    ruta = crear_csv(
        tmp_path, ";",
        filas=[["código", "título"], ["1", "Rayuela"], ["2", "El Aleph"]],
        encoding="cp1252",
    )

    with pytest.raises(UnicodeDecodeError):
        analizar_csv(ruta)


def test_limitacion_un_archivo_vacio_falla_con_un_error_de_csv(tmp_path):
    ruta = tmp_path / "vacio.csv"
    ruta.write_text("", encoding="utf-8")

    with pytest.raises(csv.Error):
        analizar_csv(ruta)


def test_limitacion_detectar_columnas_en_un_archivo_vacio_produce_stopiteration(tmp_path):
    ruta = tmp_path / "vacio.csv"
    ruta.write_text("", encoding="utf-8")

    with pytest.raises(StopIteration):
        detectar_columnas(ruta, ",")