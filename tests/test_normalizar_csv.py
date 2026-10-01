import csv
from pathlib import Path

import pytest

import modulos.cargadores.normalizar_csv as modulo_normalizar
from modulos.cargadores.normalizar_csv import CAMPOS_ESTANDAR, normalizar_catalogo_csv

RUTA_CATALOGO_PRUEBA_3 = (
    Path(__file__).resolve().parent.parent / "data" / "raw" / "catalogo_prueba_3.csv"
)

SEPARADORES = [",", ";", "\t", "|"]

ENCABEZADO = ["Código", "Título principal", "Responsable", "ISBN-13"]
CAMPOS = ["001", "titulo", "autor", "isbn"]
FILAS = [
    ["1", "Rayuela", "Julio Cortázar", "9780000000001"],
    ["2", "El Aleph", "Jorge Luis Borges", "9780000000002"],
    ["3", "Ficciones", "Jorge Luis Borges", "9780000000003"],
]


def csv_texto(separador, filas):
    return "".join(separador.join(fila) + "\n" for fila in filas)


def crear_csv(tmp_path, texto, encoding="utf-8"):
    ruta = tmp_path / "catalogo.csv"
    ruta.write_bytes(texto.encode(encoding))
    return ruta


def registro(campos):
    # Un registro normalizado siempre trae los 9 campos estándar.
    base = {campo: "" for campo in CAMPOS_ESTANDAR}
    base.update(campos)
    return base


# ---------- Estructura del resultado ----------

def test_devuelve_las_cuatro_claves(tmp_path):
    ruta = crear_csv(tmp_path, csv_texto(",", [ENCABEZADO] + FILAS))

    resultado = normalizar_catalogo_csv(ruta)

    assert set(resultado) == {
        "catalogo", "mapeo", "columnas_originales", "columnas_desconocidas",
    }


# ---------- Normalización con cada separador ----------

@pytest.mark.parametrize("separador", SEPARADORES)
def test_normaliza_con_cada_separador(tmp_path, separador):
    ruta = crear_csv(tmp_path, csv_texto(separador, [ENCABEZADO] + FILAS))

    resultado = normalizar_catalogo_csv(ruta)

    assert resultado["columnas_originales"] == ENCABEZADO
    assert resultado["mapeo"] == {
        "Código": "001",
        "Título principal": "titulo",
        "Responsable": "autor",
        "ISBN-13": "isbn",
    }
    assert resultado["columnas_desconocidas"] == []
    assert resultado["catalogo"] == [
        registro(dict(zip(CAMPOS, fila))) for fila in FILAS
    ]


# ---------- Campos y columnas ----------

def test_los_campos_sin_columna_quedan_vacios(tmp_path):
    ruta = crear_csv(
        tmp_path,
        "titulo,autor\nRayuela,Cortázar\nEl Aleph,Borges\nFicciones,Borges\n",
    )

    catalogo = normalizar_catalogo_csv(ruta)["catalogo"]

    assert catalogo == [
        registro({"titulo": "Rayuela", "autor": "Cortázar"}),
        registro({"titulo": "El Aleph", "autor": "Borges"}),
        registro({"titulo": "Ficciones", "autor": "Borges"}),
    ]
    assert len(catalogo[0]) == 9


def test_las_columnas_desconocidas_se_informan_y_no_pasan_al_catalogo(tmp_path):
    ruta = crear_csv(
        tmp_path,
        "001,titulo,Color de tapa,Materia\n"
        "1,Rayuela,Roja,Novela\n"
        "2,El Aleph,Azul,Cuento\n"
        "3,Ficciones,Verde,Cuento\n",
    )

    resultado = normalizar_catalogo_csv(ruta)

    assert resultado["columnas_originales"] == ["001", "titulo", "Color de tapa", "Materia"]
    assert resultado["mapeo"] == {"001": "001", "titulo": "titulo"}
    assert resultado["columnas_desconocidas"] == ["Color de tapa", "Materia"]
    for fila in resultado["catalogo"]:
        assert set(fila) == set(CAMPOS_ESTANDAR)
    assert resultado["catalogo"][0] == registro({"001": "1", "titulo": "Rayuela"})


def test_quita_los_espacios_alrededor_de_los_valores(tmp_path):
    ruta = crear_csv(
        tmp_path,
        "001,titulo,autor\n"
        "000001, Rayuela ,  Julio Cortázar  \n"
        "000002,El Aleph, Borges\n"
        "000003,Ficciones,Borges \n",
    )

    catalogo = normalizar_catalogo_csv(ruta)["catalogo"]

    assert catalogo[0] == registro(
        {"001": "000001", "titulo": "Rayuela", "autor": "Julio Cortázar"}
    )
    assert catalogo[1]["autor"] == "Borges"
    assert catalogo[2]["autor"] == "Borges"


# ---------- Catálogo de prueba real ----------
# Depende del archivo data/raw/catalogo_prueba_3.csv: es material de prueba fijo.
# Si lo cambiás a propósito, actualizá estos valores.

def test_mapeo_del_catalogo_de_prueba_3():
    resultado = normalizar_catalogo_csv(RUTA_CATALOGO_PRUEBA_3)

    assert resultado["columnas_originales"] == [
        "Código", "Título principal", "Responsable", "ISBN-13", "Publisher",
        "Año publicación", "Ubicación", "Código de barras", "Tipo de material",
    ]
    assert resultado["mapeo"] == {
        "Código": "001",
        "Título principal": "titulo",
        "Responsable": "autor",
        "ISBN-13": "isbn",
        "Publisher": "editorial",
        "Año publicación": "anio",
        "Ubicación": "ubicacion",
        "Código de barras": "codigo_barras",
        "Tipo de material": "tipo_material",
    }
    assert resultado["columnas_desconocidas"] == []


def test_primer_registro_del_catalogo_de_prueba_3():
    catalogo = normalizar_catalogo_csv(RUTA_CATALOGO_PRUEBA_3)["catalogo"]

    assert len(catalogo) == 10
    assert catalogo[0] == {
        "001": "000001",
        "titulo": "El Aleph",
        "autor": "Borges, Jorge Luis",
        "isbn": "9789500723459",
        "editorial": "Emecé",
        "anio": "1949",
        "ubicacion": "Sala A",
        "codigo_barras": "1000001",
        "tipo_material": "Libro",
    }


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

def test_limitacion_dos_columnas_del_mismo_campo_se_pisan_entre_si(tmp_path):
    # Gana siempre la última columna, aunque esté vacía.
    ruta = crear_csv(
        tmp_path,
        "001,Título,Title,autor\n"
        "1,Rayuela,Hopscotch,Cortázar\n"
        "2,El Aleph,,Borges\n"
        "3,Ficciones,Fictions,Borges\n",
    )

    resultado = normalizar_catalogo_csv(ruta)

    assert resultado["mapeo"] == {
        "001": "001", "Título": "titulo", "Title": "titulo", "autor": "autor",
    }
    assert [r["titulo"] for r in resultado["catalogo"]] == ["Hopscotch", "", "Fictions"]


def test_limitacion_un_espacio_doble_en_el_encabezado_descarta_toda_la_columna(tmp_path):
    ruta = crear_csv(
        tmp_path,
        "001,titulo,Autor  principal\n1,Rayuela,Cortázar\n2,El Aleph,Borges\n3,Ficciones,Borges\n",
    )

    resultado = normalizar_catalogo_csv(ruta)

    assert resultado["columnas_desconocidas"] == ["Autor  principal"]
    assert [r["autor"] for r in resultado["catalogo"]] == ["", "", ""]


def test_limitacion_un_archivo_guardado_como_ansi_no_se_puede_leer(tmp_path):
    ruta = crear_csv(
        tmp_path,
        "código,título\n1,Rayuela\n2,El Aleph\n3,Ficciones\n",
        encoding="cp1252",
    )

    with pytest.raises(UnicodeDecodeError):
        normalizar_catalogo_csv(ruta)


def test_limitacion_un_archivo_vacio_falla_con_un_error_de_csv(tmp_path):
    ruta = crear_csv(tmp_path, "")

    with pytest.raises(csv.Error):
        normalizar_catalogo_csv(ruta)


def test_limitacion_una_fila_con_menos_columnas_provoca_un_error(tmp_path, monkeypatch):
    # Se reemplaza analizar_csv para no depender del detector de separadores.
    monkeypatch.setattr(
        modulo_normalizar,
        "analizar_csv",
        lambda ruta: {"separador": ",", "columnas": ["001", "titulo", "autor"]},
    )
    ruta = crear_csv(tmp_path, "001,titulo,autor\n1,Rayuela\n")

    with pytest.raises(AttributeError):
        normalizar_catalogo_csv(ruta)