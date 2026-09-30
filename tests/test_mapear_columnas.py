import pytest

from modulos.cargadores.evaluar_confianza import CAMPOS_ESTANDAR
from modulos.cargadores.mapear_columnas import (
    MAPEO_COLUMNAS,
    mapear_columna,
    normalizar_nombre_columna,
    quitar_acentos,
)


# ---------- quitar_acentos ----------

@pytest.mark.parametrize("texto, esperado", [
    ("Título", "Titulo"),
    ("Código", "Codigo"),
    ("Año", "Ano"),
    ("AÑO", "ANO"),
    ("Pingüino", "Pinguino"),
    ("n\u0303", "n"),          # ñ escrita como n + tilde suelta (viene de algunos sistemas)
    ("sin acentos", "sin acentos"),
    ("", ""),
])
def test_quitar_acentos(texto, esperado):
    assert quitar_acentos(texto) == esperado


# ---------- normalizar_nombre_columna ----------

@pytest.mark.parametrize("nombre, esperado", [
    ("Título Principal", "titulo_principal"),
    ("ISBN-13", "isbn_13"),
    ("  Autor  ", "autor"),
    ("Código de barras", "codigo_de_barras"),
    ("Año publicación", "ano_publicacion"),
    ("BAR CODE", "bar_code"),
    ("Item-Type", "item_type"),
    ("", ""),
])
def test_normalizar_nombre_columna(nombre, esperado):
    assert normalizar_nombre_columna(nombre) == esperado


# ---------- mapear_columna: nombres que sí se reconocen ----------

@pytest.mark.parametrize("columna, esperado", [
    # Identificador
    ("001", "001"),
    ("ID", "001"),
    ("Código", "001"),
    ("Código registro", "001"),
    ("Id-Registro", "001"),
    # Título
    ("Título", "titulo"),
    ("Título principal", "titulo"),
    ("Título obra", "titulo"),
    ("Title", "titulo"),
    # Autor
    ("Autor", "autor"),
    ("Autor principal", "autor"),
    ("Responsable", "autor"),
    ("AUTHOR", "autor"),
    # ISBN
    ("ISBN", "isbn"),
    ("ISBN13", "isbn"),
    ("ISBN-13", "isbn"),
    ("isbn_13", "isbn"),
    ("ISBN 13", "isbn"),
    # Editorial
    ("Editorial", "editorial"),
    ("Editor", "editorial"),
    ("Publisher", "editorial"),
    # Año
    ("Año", "anio"),
    ("Ano", "anio"),
    ("Anio", "anio"),
    ("Año publicación", "anio"),
    ("Ano publicacion", "anio"),
    ("Year", "anio"),
    # Ubicación
    ("Ubicación", "ubicacion"),
    ("Ubicación física", "ubicacion"),
    ("Localización", "ubicacion"),
    ("Location", "ubicacion"),
    # Código de barras
    ("Código de barras", "codigo_barras"),
    ("Código barras", "codigo_barras"),
    ("Barcode", "codigo_barras"),
    ("Bar code", "codigo_barras"),
    # Tipo de material
    ("Tipo de material", "tipo_material"),
    ("Tipo material", "tipo_material"),
    ("Material", "tipo_material"),
    ("Item type", "tipo_material"),
])
def test_mapea_columnas_conocidas(columna, esperado):
    assert mapear_columna(columna) == esperado


@pytest.mark.parametrize("columna", ["Campo desconocido", "", "   "])
def test_columna_desconocida_devuelve_none(columna):
    assert mapear_columna(columna) is None


# ---------- Coherencia del diccionario ----------

@pytest.mark.parametrize("clave, campo", list(MAPEO_COLUMNAS.items()))
def test_cada_clave_del_diccionario_se_mapea_a_su_campo(clave, campo):
    # Si una clave tuviera mayúsculas, tildes o espacios, nunca se podría
    # encontrar, porque la búsqueda se hace con el nombre ya normalizado.
    assert mapear_columna(clave) == campo


def test_todos_los_campos_de_destino_son_campos_estandar():
    assert set(MAPEO_COLUMNAS.values()) <= CAMPOS_ESTANDAR | {"001"}


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

@pytest.mark.parametrize("columna", [
    "Materia",
    "ISBN-10",
    "ISBN10",
    "Año de publicación",
    "Nombre del libro",
])
def test_limitacion_columnas_que_evaluar_confianza_conoce_pero_este_mapeo_no(columna):
    assert mapear_columna(columna) is None


def test_limitacion_ninguna_columna_se_mapea_al_campo_materia():
    assert CAMPOS_ESTANDAR - set(MAPEO_COLUMNAS.values()) == {"materia"}


def test_limitacion_los_espacios_repetidos_no_se_unifican():
    assert normalizar_nombre_columna("Autor  principal") == "autor__principal"
    assert mapear_columna("Autor  principal") is None


def test_limitacion_un_nombre_de_columna_none_produce_un_error():
    with pytest.raises(AttributeError):
        mapear_columna(None)