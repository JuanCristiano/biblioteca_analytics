import pytest

from comparar_autores import comparar_multiples_autores

BORGES_BIOY = "Jorge Luis Borges; Adolfo Bioy Casares"


# ---------- COINCIDE ----------

@pytest.mark.parametrize("catalogo, fuente", [
    (BORGES_BIOY, BORGES_BIOY),
    (BORGES_BIOY, "Adolfo Bioy Casares; Jorge Luis Borges"),
    (BORGES_BIOY, "Borges, Jorge Luis; Bioy Casares, Adolfo"),
    (BORGES_BIOY, "Jorge Luis Borges / Adolfo Bioy Casares"),
    (BORGES_BIOY, "Jorge Luis Borges y Adolfo Bioy Casares"),
    ("JORGE LUIS BORGES; ADOLFO BIOY CASARES", "jorge luis borges; adolfo bioy casares"),
    ("Jorge   Luis   Borges; Adolfo   Bioy   Casares", BORGES_BIOY),
])
def test_coincide(catalogo, fuente):
    resultado = comparar_multiples_autores(catalogo, fuente)

    assert resultado["resultado"] == "COINCIDE"
    assert resultado["motivo"] is None
    assert len(resultado["coincidencias"]) == 2
    assert resultado["posibles_coincidencias"] == []
    assert resultado["faltantes"] == []
    assert resultado["adicionales"] == []


def test_separadores_mezclados_con_tres_autores():
    resultado = comparar_multiples_autores(
        "Jorge Luis Borges; Adolfo Bioy Casares; Julio Cortázar",
        "Julio Cortázar / Jorge Luis Borges y Adolfo Bioy Casares",
    )

    assert resultado["resultado"] == "COINCIDE"
    assert resultado["cantidad_catalogo"] == 3
    assert resultado["cantidad_fuente"] == 3
    assert len(resultado["coincidencias"]) == 3


def test_con_orden_distinto_cada_autor_se_empareja_con_su_par():
    resultado = comparar_multiples_autores(
        BORGES_BIOY, "Adolfo Bioy Casares; Jorge Luis Borges"
    )

    pares = {(c["catalogo"], c["fuente"]) for c in resultado["coincidencias"]}
    assert pares == {
        ("Jorge Luis Borges", "Jorge Luis Borges"),
        ("Adolfo Bioy Casares", "Adolfo Bioy Casares"),
    }


# ---------- POSIBLE COINCIDENCIA ----------

@pytest.mark.parametrize("catalogo, fuente", [
    (BORGES_BIOY, "Jorge Luis Borge; Adolfo Bioy Casares"),
    (BORGES_BIOY, "Jorge Luis Borge; Adolfo Bioy Cazares"),
])
def test_errores_de_escritura_son_posible_coincidencia(catalogo, fuente):
    resultado = comparar_multiples_autores(catalogo, fuente)

    assert resultado["resultado"] == "POSIBLE COINCIDENCIA"
    assert resultado["motivo"] == "POSIBLE_VARIANTE"
    assert resultado["faltantes"] == []
    assert resultado["adicionales"] == []


def test_un_error_de_escritura_separa_coincidencia_y_posible():
    resultado = comparar_multiples_autores(
        BORGES_BIOY, "Jorge Luis Borge; Adolfo Bioy Casares"
    )

    assert len(resultado["coincidencias"]) == 1
    assert resultado["coincidencias"][0]["catalogo"] == "Adolfo Bioy Casares"

    assert len(resultado["posibles_coincidencias"]) == 1
    posible = resultado["posibles_coincidencias"][0]
    assert posible["catalogo"] == "Jorge Luis Borges"
    assert posible["fuente"] == "Jorge Luis Borge"
    assert 0.85 <= posible["similitud"] < 1.0


# ---------- REVISAR ----------

@pytest.mark.parametrize("catalogo, fuente, motivo, faltantes, adicionales", [
    (BORGES_BIOY, "Jorge Luis Borges",
     "AUTOR_FALTANTE", ["Adolfo Bioy Casares"], []),
    ("Jorge Luis Borges", BORGES_BIOY,
     "AUTOR_ADICIONAL", [], ["Adolfo Bioy Casares"]),
    (BORGES_BIOY, "Jorge Luis Borges; Julio Cortázar",
     "DIFERENCIA_EN_AUTORES", ["Adolfo Bioy Casares"], ["Julio Cortázar"]),
    ("Jorge Luis Borges", "Jorge Luis Borges; Jorge Luis Borges",
     "AUTOR_ADICIONAL", [], ["Jorge Luis Borges"]),
])
def test_revisar_con_su_motivo(catalogo, fuente, motivo, faltantes, adicionales):
    resultado = comparar_multiples_autores(catalogo, fuente)

    assert resultado["resultado"] == "REVISAR"
    assert resultado["motivo"] == motivo
    assert resultado["faltantes"] == faltantes
    assert resultado["adicionales"] == adicionales


# ---------- NO DISPONIBLE ----------

@pytest.mark.parametrize("catalogo, fuente", [
    ("", "Jorge Luis Borges"),
    (None, "Jorge Luis Borges"),
    ("Jorge Luis Borges", ""),
    ("Jorge Luis Borges", None),
    ("", ""),
    (None, None),
    ("   ", "Jorge Luis Borges"),
])
def test_datos_faltantes_son_no_disponible(catalogo, fuente):
    resultado = comparar_multiples_autores(catalogo, fuente)

    assert resultado["resultado"] == "NO DISPONIBLE"
    assert resultado["motivo"] == "DATOS_FALTANTES"


def test_datos_faltantes_igual_informa_la_cantidad_de_cada_lado():
    sin_catalogo = comparar_multiples_autores("", "Jorge Luis Borges")
    sin_fuente = comparar_multiples_autores("Jorge Luis Borges", None)

    assert (sin_catalogo["cantidad_catalogo"], sin_catalogo["cantidad_fuente"]) == (0, 1)
    assert (sin_fuente["cantidad_catalogo"], sin_fuente["cantidad_fuente"]) == (1, 0)


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

def test_limitacion_iniciales_no_se_reconocen():
    resultado = comparar_multiples_autores(BORGES_BIOY, "J. L. Borges; A. Bioy Casares")

    assert resultado["resultado"] == "REVISAR"
    assert resultado["motivo"] == "DIFERENCIA_EN_AUTORES"
    assert "Jorge Luis Borges" in resultado["faltantes"]


def test_limitacion_la_coma_no_separa_autores():
    resultado = comparar_multiples_autores(
        "Jorge Luis Borges, Adolfo Bioy Casares", BORGES_BIOY
    )

    assert resultado["cantidad_catalogo"] == 1
    assert resultado["cantidad_fuente"] == 2
    assert resultado["resultado"] == "REVISAR"
    assert resultado["motivo"] == "DIFERENCIA_EN_AUTORES"


def test_limitacion_siglas_no_se_relacionan_con_su_nombre_completo():
    resultado = comparar_multiples_autores(
        "UNESCO",
        "United Nations Educational, Scientific and Cultural Organization",
    )

    assert resultado["resultado"] == "REVISAR"
    assert resultado["motivo"] == "DIFERENCIA_EN_AUTORES"