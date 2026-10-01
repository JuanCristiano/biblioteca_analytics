import copy

import pytest

from modulos.comparacion.comparador_bibliografico import (
    autores_coinciden,
    comparar_registro,
    textos_coinciden,
)

CATALOGO = {
    "isbn": "9780140328721",
    "titulo": "Fantastic Mr. Fox",
    "autor": "ROALD DAHL",
    "editorial": "puffin",
}


def armar_externo(**cambios):
    datos = {
        "isbn": "9780140328721",
        "titulo": "Fantastic Mr Fox",
        "autores": ["Roald Dahl"],
        "editoriales": ["Puffin"],
    }
    datos.update(cambios)
    return datos


# ---------- textos_coinciden ----------

@pytest.mark.parametrize("valor, externos, esperado", [
    ("puffin", ["Puffin"], True),
    ("Cien años de soledad", ["Cien anos de soledad"], True),
    ("Editorial B", ["Editorial A", "editorial b"], True),
    ("puffin", ["Penguin"], False),
    ("puffin", [], None),
    ("puffin", None, None),
    ("", ["Puffin"], None),
    (None, ["Puffin"], None),
    ("   ", ["Puffin"], None),
])
def test_textos_coinciden(valor, externos, esperado):
    assert textos_coinciden(valor, externos) is esperado


def test_limitacion_textos_coinciden_exige_igualdad_completa():
    assert textos_coinciden("Puffin Books", ["Puffin"]) is False


# ---------- autores_coinciden ----------

@pytest.mark.parametrize("autor, externos, esperado", [
    ("ROALD DAHL", ["Dahl, Roald"], True),
    ("Gabriel García Márquez", ["García Márquez, Gabriel"], True),
    ("Dahl, Roald", ["Roald Dahl"], True),
    ("Roald Dahl", ["Julio Cortázar", "Roald Dahl"], True),
    ("Roald Dahl", ["Julio Cortázar"], False),
    ("Roald Dahl", [], None),
    ("Roald Dahl", None, None),
    ("", ["Roald Dahl"], None),
    (None, ["Roald Dahl"], None),
])
def test_autores_coinciden(autor, externos, esperado):
    assert autores_coinciden(autor, externos) is esperado


def test_limitacion_autores_coinciden_no_tolera_errores_de_tipeo():
    assert autores_coinciden("Roald Dalh", ["Roald Dahl"]) is False


# ---------- ISBN dentro de comparar_registro ----------

@pytest.mark.parametrize("isbn_catalogo, isbn_externo, esperado", [
    ("9780140328721", "9780140328721", True),
    ("978-0-14-032872-1", "9780140328721", True),
    ("ISBN 978-0-14-032872-1", "9780140328721", True),
    ("080442957x", "080442957X", True),
    ("9780140328721", "9780140328722", False),
])
def test_comparacion_de_isbn(isbn_catalogo, isbn_externo, esperado):
    resultado = comparar_registro({"isbn": isbn_catalogo}, {"isbn": isbn_externo})

    assert resultado["isbn"] is esperado


@pytest.mark.parametrize("catalogo, externo", [
    ({"isbn": "9780140328721"}, {}),
    ({}, {"isbn": "9780140328721"}),
    ({"isbn": ""}, {"isbn": "9780140328721"}),
])
def test_isbn_sin_dato_de_un_lado_no_se_compara(catalogo, externo):
    assert comparar_registro(catalogo, externo)["isbn"] is None


def test_limitacion_isbn10_e_isbn13_del_mismo_libro_se_consideran_distintos():
    resultado = comparar_registro({"isbn": "0-306-40615-2"}, {"isbn": "978-0-306-40615-7"})

    assert resultado["isbn"] is False


# ---------- comparar_registro ----------

def test_coincide_cuando_los_cuatro_campos_coinciden():
    resultado = comparar_registro(CATALOGO, armar_externo())

    assert resultado == {
        "isbn": True,
        "titulo": True,
        "autor": True,
        "editorial": True,
        "resultado": "COINCIDE",
    }


@pytest.mark.parametrize("cambios, campo_sin_dato", [
    ({"isbn": None}, "isbn"),
    ({"editoriales": []}, "editorial"),
])
def test_coincide_parcialmente_si_falta_un_dato(cambios, campo_sin_dato):
    resultado = comparar_registro(CATALOGO, armar_externo(**cambios))

    assert resultado[campo_sin_dato] is None
    assert resultado["resultado"] == "COINCIDE PARCIALMENTE"


@pytest.mark.parametrize("cambios, campo", [
    ({"isbn": "9780140328722"}, "isbn"),
    ({"titulo": "Otro libro"}, "titulo"),
    ({"autores": ["Julio Cortázar"]}, "autor"),
    ({"editoriales": ["Penguin"]}, "editorial"),
])
def test_una_discrepancia_en_cualquier_campo_pide_revision(cambios, campo):
    resultado = comparar_registro(CATALOGO, armar_externo(**cambios))

    assert resultado[campo] is False
    assert resultado["resultado"] == "REVISAR"


def test_un_titulo_con_error_de_tipeo_pide_revision():
    catalogo = {**CATALOGO, "titulo": "  Fantastic    Mr. Foz  "}

    resultado = comparar_registro(catalogo, armar_externo())

    assert resultado["titulo"] is False
    assert resultado["isbn"] is True
    assert resultado["autor"] is True
    assert resultado["editorial"] is True
    assert resultado["resultado"] == "REVISAR"


def test_una_discrepancia_alcanza_aunque_los_demas_campos_no_tengan_datos():
    resultado = comparar_registro(
        {"isbn": "9780140328721"}, {"isbn": "9780140328722"}
    )

    assert resultado == {
        "isbn": False,
        "titulo": None,
        "autor": None,
        "editorial": None,
        "resultado": "REVISAR",
    }


def test_sin_datos_de_la_fuente_externa():
    # Es lo que devuelve la consulta cuando Open Library no responde.
    externo = {"fuente": "Open Library", "encontrado": False, "error": "Error de conexión"}

    resultado = comparar_registro(CATALOGO, externo)

    assert resultado == {
        "isbn": None,
        "titulo": None,
        "autor": None,
        "editorial": None,
        "resultado": "SIN DATOS PARA COMPARAR",
    }


def test_registros_vacios():
    assert comparar_registro({}, {})["resultado"] == "SIN DATOS PARA COMPARAR"


def test_no_modifica_ninguno_de_los_registros():
    catalogo = copy.deepcopy(CATALOGO)
    externo = armar_externo()
    copia_externo = copy.deepcopy(externo)

    comparar_registro(catalogo, externo)

    assert catalogo == CATALOGO
    assert externo == copia_externo