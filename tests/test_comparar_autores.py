import pytest

from comparar_autores import (
    comparar_autor,
    normalizar_autor,
    reordenar_autor,
    separar_autores,
)


# ---------- normalizar_autor ----------

@pytest.mark.parametrize("autor, esperado", [
    ("Gabriel García Márquez", "gabriel garcia marquez"),
    ("Borges, Jorge Luis.", "borges jorge luis"),
    ("  Jorge   Luis  ", "jorge luis"),
    ("J.L. Borges", "j l borges"),
    (None, ""),
])
def test_normalizar_autor(autor, esperado):
    assert normalizar_autor(autor) == esperado


# ---------- reordenar_autor ----------

@pytest.mark.parametrize("autor, esperado", [
    ("Dahl, Roald", "Roald Dahl"),
    ("Roald Dahl", "Roald Dahl"),
    ("Cervantes, Miguel de", "Miguel de Cervantes"),
    ("  Dahl ,  Roald  ", "Roald Dahl"),
    ("", ""),
    (None, ""),
])
def test_reordenar_autor(autor, esperado):
    assert reordenar_autor(autor) == esperado


# ---------- separar_autores ----------

DOS_AUTORES = ["Jorge Luis Borges", "Adolfo Bioy Casares"]


@pytest.mark.parametrize("campo, esperado", [
    ("Jorge Luis Borges; Adolfo Bioy Casares", DOS_AUTORES),
    ("Jorge Luis Borges / Adolfo Bioy Casares", DOS_AUTORES),
    ("Jorge Luis Borges y Adolfo Bioy Casares", DOS_AUTORES),
    ("Jorge Luis Borges Y Adolfo Bioy Casares", DOS_AUTORES),
    (" Borges ; Bioy ", ["Borges", "Bioy"]),
    ("Borges;;Bioy;", ["Borges", "Bioy"]),
    ("Jorge Luis Borges", ["Jorge Luis Borges"]),
    (None, []),
    ("", []),
    ("   ", []),
])
def test_separar_autores(campo, esperado):
    assert separar_autores(campo) == esperado


def test_la_coma_no_separa_autores():
    # La coma queda reservada para el formato "Apellido, Nombre".
    campo = "Jorge Luis Borges, Adolfo Bioy Casares"
    assert separar_autores(campo) == [campo]


# ---------- comparar_autor ----------

@pytest.mark.parametrize("catalogo, fuente", [
    ("Roald Dahl", "Roald Dahl"),
    ("Roald Dahl", "Dahl, Roald"),
    ("Dahl, Roald", "Roald Dahl"),
    ("Gabriel García Márquez", "García Márquez, Gabriel"),
    ("Mario Vargas Llosa", "Vargas Llosa, Mario"),
    ("Gabriel García Márquez", "Gabriel Garcia Marquez"),
    ("Julio Cortázar", "Julio Cortazar"),
    ("ROALD DAHL", "roald dahl"),
    ("GABRIEL GARCÍA MÁRQUEZ", "Gabriel García Márquez"),
    ("Jorge Luis Borges.", "Jorge Luis Borges"),
    ("Borges, Jorge Luis.", "Borges, Jorge Luis"),
    ("Gabriel García Marquéz", "Gabriel García Márquez"),
    ("Gabriel José García Márquez", "García Márquez, Gabriel José"),
    ("Miguel de Cervantes", "Cervantes, Miguel de"),
    ("de Cervantes, Miguel", "Miguel de Cervantes"),
    ("  Roald Dahl  ", "Roald Dahl"),
    ("Gabriel    García    Márquez", "García Márquez, Gabriel"),
    ("Organizacion Mundial de la Salud", "Organización Mundial de la Salud"),
])
def test_coincide(catalogo, fuente):
    resultado = comparar_autor(catalogo, fuente)

    assert resultado["resultado"] == "COINCIDE"
    assert resultado["similitud"] == 1.0


@pytest.mark.parametrize("catalogo, fuente", [
    ("Roald Dalh", "Roald Dahl"),
    ("Jorge Luis Borge", "Jorge Luis Borges"),
    ("Jorge L. Borges", "Jorge Luis Borges"),
    ("Gabriel García Márquez", "García Márquez, Gabriel José"),
    ("Gabriel García Márquez", "Gabriel García Marqués"),
    ("Mario Vargas Llosa", "Mario Vargas Losa"),
])
def test_posible_coincidencia(catalogo, fuente):
    resultado = comparar_autor(catalogo, fuente)

    assert resultado["resultado"] == "POSIBLE COINCIDENCIA"
    assert 0.85 <= resultado["similitud"] < 1.0


@pytest.mark.parametrize("catalogo, fuente", [
    ("Roald Dahl", "Julio Cortázar"),
    ("Jorge Luis Borges", "Gabriel García Márquez"),
    ("Mario Vargas Llosa", "José Saramago"),
])
def test_autores_distintos_no_coinciden(catalogo, fuente):
    resultado = comparar_autor(catalogo, fuente)

    assert resultado["resultado"] == "NO COINCIDE"
    assert resultado["similitud"] < 0.85


@pytest.mark.parametrize("catalogo, fuente", [
    ("", "Roald Dahl"),
    (None, "Roald Dahl"),
    ("Roald Dahl", ""),
    ("Roald Dahl", None),
    ("", ""),
    (None, None),
    ("   ", "Roald Dahl"),
])
def test_datos_faltantes_son_no_disponible(catalogo, fuente):
    resultado = comparar_autor(catalogo, fuente)

    assert resultado["resultado"] == "NO DISPONIBLE"
    assert resultado["similitud"] is None
    assert resultado["catalogo_normalizado"] == ""
    assert resultado["fuente_normalizada"] == ""


def test_el_resultado_conserva_los_originales_y_agrega_los_normalizados():
    resultado = comparar_autor("Gabriel García Márquez", "García Márquez, Gabriel")

    assert resultado["autor_catalogo"] == "Gabriel García Márquez"
    assert resultado["autor_fuente"] == "García Márquez, Gabriel"
    assert resultado["catalogo_normalizado"] == "gabriel garcia marquez"
    assert resultado["fuente_normalizada"] == "gabriel garcia marquez"
    assert resultado["similitud"] == 1.0
    assert resultado["resultado"] == "COINCIDE"


# ---------- Limitaciones conocidas ----------
# Estos tests documentan lo que la función hace HOY, aunque no sea lo ideal.
# Si mejorás la función y alguno falla, es una buena noticia: actualizá el test.

@pytest.mark.parametrize("catalogo, fuente", [
    ("J. L. Borges", "Jorge Luis Borges"),
    ("G. García Márquez", "Gabriel García Márquez"),
    ("Borges, J.", "Jorge Luis Borges"),
    ("Jorge Francisco Isidoro Luis Borges", "Borges, Jorge Luis"),
    ("UNESCO", "United Nations Educational, Scientific and Cultural Organization"),
])
def test_limitacion_iniciales_nombres_largos_y_siglas(catalogo, fuente):
    assert comparar_autor(catalogo, fuente)["resultado"] == "NO COINCIDE"


def test_limitacion_la_y_separa_apellidos_como_ortega_y_gasset():
    assert separar_autores("José Ortega y Gasset") == ["José Ortega", "Gasset"]


def test_limitacion_con_mas_de_una_coma_no_reordena():
    autor = "García Márquez, Gabriel, 1927-2014"
    assert reordenar_autor(autor) == autor