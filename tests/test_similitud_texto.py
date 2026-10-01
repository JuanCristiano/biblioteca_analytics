import pytest

from modulos.comparacion.similitud_texto import (
    calcular_similitud,
    distancia_levenshtein,
    normalizar_texto,
)


def test_normalizar_quita_tildes_mayusculas_y_puntuacion():
    assert normalizar_texto("Gabriel García Márquez") == "gabriel garcia marquez"
    assert normalizar_texto("Fantastic Mr. Fox") == "fantastic mr fox"


def test_normalizar_reduce_espacios_y_signos():
    assert normalizar_texto("  Hola,   MUNDO!!  ") == "hola mundo"


def test_normalizar_none_devuelve_texto_vacio():
    assert normalizar_texto(None) == ""


@pytest.mark.parametrize("texto1, texto2, esperada", [
    ("kitten", "sitting", 3),
    ("fox", "foz", 1),
    ("abc", "", 3),
    ("", "abc", 3),
    ("igual", "IGUAL", 0),
])
def test_distancia_levenshtein(texto1, texto2, esperada):
    assert distancia_levenshtein(texto1, texto2) == esperada


@pytest.mark.parametrize("texto1, texto2, esperada", [
    ("Fantastic Mr. Fox", "Fantastic Mr Fox", 1.0),
    ("Fantastic Mr. Fox", "Fantastic Mr. Foz", 1 - 1 / 16),
    ("Fantastic Mr. Fox", "Fantastic Mr. Foxx", 1 - 1 / 17),
    ("Roald Dahl", "Roald Dhal", 0.8),
    ("Gabriel García Márquez", "Gabriel Garcia Marquez", 1.0),
    ("Gabriel García Márquez", "Gabriel Garcia Marque", 1 - 1 / 22),
    ("Gabriel García Márquez", "Gabriel García Marquez", 1.0),
    ("Gabriel García Márquez", "Gabrial García Márquez", 1 - 1 / 22),
])
def test_similitud_de_variantes_parecidas(texto1, texto2, esperada):
    assert calcular_similitud(texto1, texto2) == pytest.approx(esperada)


@pytest.mark.parametrize("texto1, texto2", [
    ("Fantastic Mr. Fox", "Charlie y la fábrica de chocolate"),
    ("Roald Dahl", "J. K. Rowling"),
])
def test_textos_distintos_tienen_similitud_baja(texto1, texto2):
    assert calcular_similitud(texto1, texto2) < 0.3


def test_nombre_con_orden_invertido_tiene_similitud_baja():
    # Limitación conocida: esta función no reconoce "Apellido, Nombre".
    assert calcular_similitud("Gabriel García Márquez", "García Márquez, Gabriel") < 0.5


def test_textos_vacios():
    assert calcular_similitud("", "") == 1.0
    assert calcular_similitud(None, None) == 1.0
    assert calcular_similitud("algo", "") == 0.0


def test_la_similitud_es_simetrica():
    assert calcular_similitud("Roald Dahl", "Roald Dhal") == calcular_similitud("Roald Dhal", "Roald Dahl")