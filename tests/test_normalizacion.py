import pytest

from normalizacion import normalizar_autor, normalizar_texto


def test_normalizar_texto_quita_tildes_mayusculas_y_puntuacion():
    assert normalizar_texto("Gabriel García Márquez") == "gabriel garcia marquez"
    assert normalizar_texto("  Hola,   MUNDO!!  ") == "hola mundo"


def test_normalizar_texto_none_devuelve_texto_vacio():
    assert normalizar_texto(None) == ""


@pytest.mark.parametrize("autor", [
    "Gabriel García Márquez",
    "Gabriel Garcia Marquez",
    "García Márquez, Gabriel",
    "Garcia Marquez, Gabriel",
])
def test_formas_con_y_sin_coma_dan_el_mismo_resultado(autor):
    assert normalizar_autor(autor) == "gabriel garcia marquez"


def test_sin_coma_no_reordena_el_nombre():
    # Limitación conocida: sin coma no hay forma de saber cuál es el apellido.
    assert normalizar_autor("García Márquez Gabriel") == "garcia marquez gabriel"


def test_un_error_de_tipeo_se_conserva():
    # Corregir tipeos es tarea de la comparación por similitud, no de la normalización.
    assert normalizar_autor("Gabrial García Márquez") == "gabrial garcia marquez"


@pytest.mark.parametrize("valor", [None, "", "   "])
def test_valores_vacios_devuelven_texto_vacio(valor):
    assert normalizar_autor(valor) == ""


@pytest.mark.parametrize("valor, esperado", [
    ("García Márquez,", "garcia marquez"),
    (", Gabriel", "gabriel"),
])
def test_coma_con_una_de_las_partes_vacia(valor, esperado):
    assert normalizar_autor(valor) == esperado


def test_apellido_y_nombre_compuestos():
    assert normalizar_autor("de la Cruz, Sor Juana Inés") == "sor juana ines de la cruz"