import pytest

from modulos.cargadores.evaluar_confianza import (
    CAMPOS_ESTANDAR,
    EQUIVALENCIAS_CONOCIDAS,
    SINONIMOS,
    TERMINOS_INCOMPATIBLES,
    buscar_mejor_coincidencia,
    calcular_similitud,
    construir_candidatos,
    es_incompatible,
    evaluar_mapeo,
    normalizar_nombre_columna,
)


def evaluar(columna, campo):
    return evaluar_mapeo({columna: campo})[0]


# ---------- normalizar_nombre_columna ----------

@pytest.mark.parametrize("nombre, esperado", [
    ("Título Principal", "titulo principal"),
    ("ISBN-13", "isbn 13"),
    ("codigo_barras", "codigo barras"),
    ("  Año   de   publicación  ", "ano de publicacion"),
    ("ÁREA TEMÁTICA", "area tematica"),
])
def test_normalizar_nombre_columna(nombre, esperado):
    assert normalizar_nombre_columna(nombre) == esperado


# ---------- calcular_similitud ----------

def test_similitud_ignora_tildes_y_mayusculas():
    assert calcular_similitud("Título", "titulo") == 1.0


def test_similitud_de_un_error_de_tipeo():
    assert calcular_similitud("ISN", "isbn") == pytest.approx(6 / 7)


# ---------- es_incompatible ----------

@pytest.mark.parametrize("columna, campo, esperado", [
    ("ISSN", "isbn", True),
    ("issn 10", "isbn", True),
    ("ISSN-13", "isbn", True),
    ("Autoridad", "autor", True),
    ("Autorización", "autor", True),
    ("ISBN", "isbn", False),
    ("Autor", "autor", False),
    ("ISSN", "autor", False),
    ("ISSN", "campo_inexistente", False),
])
def test_es_incompatible(columna, campo, esperado):
    assert es_incompatible(columna, campo) is esperado


# ---------- buscar_mejor_coincidencia ----------

def test_mejor_coincidencia_para_un_error_de_tipeo():
    candidato, similitud = buscar_mejor_coincidencia("ISN", "isbn")

    assert candidato == "isbn"
    assert similitud == pytest.approx(6 / 7)


def test_mejor_coincidencia_con_tilde_o_sin_tilde_da_la_misma_similitud():
    # No se compara el nombre del candidato: "titulo" y "título" empatan
    # y cuál se elige depende del orden interno de un conjunto (set).
    candidato, similitud = buscar_mejor_coincidencia("Titlo", "titulo")

    assert normalizar_nombre_columna(candidato) == "titulo"
    assert similitud == pytest.approx(10 / 11)


def test_mejor_coincidencia_con_un_campo_desconocido():
    assert buscar_mejor_coincidencia("cualquier cosa", "campo_inexistente") == (None, 0)


# ---------- construir_candidatos ----------

def test_candidatos_incluyen_todos_los_campos_estandar():
    candidatos = construir_candidatos()

    assert set(CAMPOS_ESTANDAR) <= set(candidatos)
    for campo in CAMPOS_ESTANDAR:
        assert campo in candidatos[campo]


def test_candidatos_incluyen_equivalencias_y_sinonimos():
    candidatos = construir_candidatos()

    assert "Título principal" in candidatos["titulo"]
    assert "nombre del libro" in candidatos["titulo"]
    assert "Código" in candidatos["001"]


# ---------- Coherencia de los diccionarios de datos ----------

def test_todos_los_sinonimos_apuntan_a_un_campo_estandar():
    assert set(SINONIMOS.values()) <= set(CAMPOS_ESTANDAR)


def test_todas_las_equivalencias_apuntan_a_un_campo_estandar_o_al_001():
    assert set(EQUIVALENCIAS_CONOCIDAS.values()) - {"001"} <= set(CAMPOS_ESTANDAR)


def test_los_terminos_incompatibles_pertenecen_a_campos_estandar():
    assert set(TERMINOS_INCOMPATIBLES) <= set(CAMPOS_ESTANDAR)


def test_los_nombres_conocidos_no_se_contradicen():
    campo_por_nombre = {}
    for diccionario in (EQUIVALENCIAS_CONOCIDAS, SINONIMOS):
        for nombre, campo in diccionario.items():
            normalizado = normalizar_nombre_columna(nombre)
            assert campo_por_nombre.setdefault(normalizado, campo) == campo, nombre


# ---------- evaluar_mapeo: nivel 0, nombre estándar exacto ----------

@pytest.mark.parametrize("columna, campo", [
    ("Título", "titulo"),
    ("ISBN", "isbn"),
    ("  AUTOR  ", "autor"),
    ("Materia", "materia"),
    ("anio", "anio"),
    ("Ubicación", "ubicacion"),
])
def test_nombre_estandar_exacto(columna, campo):
    resultado = evaluar(columna, campo)

    assert resultado["confianza"] == "ALTA"
    assert resultado["motivo"] == "nombre estándar exacto"


# ---------- nivel 1, equivalencia conocida ----------

@pytest.mark.parametrize("columna, campo", [
    ("Título principal", "titulo"),
    ("Responsable", "autor"),
    ("responsable", "autor"),
    ("RESPONSABLE", "autor"),
    ("ISBN-13", "isbn"),
    ("Publisher", "editorial"),
    ("Año publicación", "anio"),
    ("Código", "001"),
    ("Código de barras", "codigo_barras"),
    ("Tipo de material", "tipo_material"),
])
def test_equivalencia_conocida(columna, campo):
    resultado = evaluar(columna, campo)

    assert resultado["confianza"] == "ALTA"
    assert resultado["motivo"] == "equivalencia conocida"


# ---------- nivel 2, sinónimo o variante ----------

@pytest.mark.parametrize("columna, campo", [
    ("Nombre del libro", "titulo"),
    ("Autor principal", "autor"),
    ("Editor", "editorial"),
    ("Autores", "autor"),
    ("Nombre del autor", "autor"),
    ("Asignatura", "materia"),
    ("Materia bibliográfica", "materia"),
    ("Área temática", "materia"),
    ("ISBN10", "isbn"),
])
def test_sinonimo_o_variante_conocida(columna, campo):
    resultado = evaluar(columna, campo)

    assert resultado["confianza"] == "MEDIA"
    assert resultado["motivo"] == "sinónimo o variante conocida"


# ---------- nivel 3, término incompatible ----------

@pytest.mark.parametrize("columna, campo", [
    ("ISSN", "isbn"),
    ("Autoridad", "autor"),
    ("Autorización", "autor"),
])
def test_termino_incompatible(columna, campo):
    resultado = evaluar(columna, campo)

    assert resultado["confianza"] == "BAJA"
    assert resultado["motivo"] == "término incompatible con el campo estándar"


# ---------- nivel 4, posible error de escritura ----------
# El nombre del candidato no se compara: cuando dos candidatos empatan
# (por ejemplo "titulo" y "título") cambia entre ejecuciones.

@pytest.mark.parametrize("columna, campo, porcentaje", [
    ("ResponsabIe", "autor", "91%"),
    ("Responsabl", "autor", "95%"),
    ("Responable", "autor", "95%"),
    ("Titlo", "titulo", "91%"),
    ("Titulu", "titulo", "83%"),
    ("Títul", "titulo", "91%"),
    ("ISN", "isbn", "86%"),
])
def test_posible_error_de_escritura(columna, campo, porcentaje):
    resultado = evaluar(columna, campo)

    assert resultado["confianza"] == "MEDIA"
    assert resultado["motivo"].startswith("posible error de escritura; similar a '")
    assert resultado["motivo"].endswith(f"({porcentaje})")


# ---------- nivel 5, sin correspondencia ----------

@pytest.mark.parametrize("columna, campo", [
    ("Color de tapa", "titulo"),
    ("Apellido del autor", "autor"),
    ("Responsable", "titulo"),
    ("Columna rara", "campo_inexistente"),
])
def test_sin_correspondencia_confiable(columna, campo):
    resultado = evaluar(columna, campo)

    assert resultado["confianza"] == "BAJA"
    assert resultado["motivo"] == "sin correspondencia confiable"


# ---------- Estructura del resultado ----------

def test_devuelve_un_resultado_por_columna_en_el_mismo_orden():
    mapeo = {"Responsable": "autor", "Color de tapa": "titulo", "ISBN": "isbn"}

    resultados = evaluar_mapeo(mapeo)

    assert [r["columna_original"] for r in resultados] == list(mapeo)
    assert [r["campo_estandar"] for r in resultados] == ["autor", "titulo", "isbn"]
    assert [r["confianza"] for r in resultados] == ["ALTA", "BAJA", "ALTA"]
    for r in resultados:
        assert set(r) == {"columna_original", "campo_estandar", "confianza", "motivo"}


def test_mapeo_vacio():
    assert evaluar_mapeo({}) == []


# ---------- Limitación conocida ----------

@pytest.mark.parametrize("columna", ["codigo_barras", "tipo_material"])
def test_limitacion_el_nombre_tecnico_con_guion_bajo_no_es_nombre_exacto(columna):
    # La columna se normaliza a "codigo barras" y ya no es igual al campo
    # "codigo_barras", así que se resuelve como sinónimo (MEDIA) y no como exacto (ALTA).
    resultado = evaluar(columna, columna)

    assert resultado["confianza"] == "MEDIA"
    assert resultado["motivo"] == "sinónimo o variante conocida"