import pytest

from comparar_titulos import comparar_titulo, normalizar_titulo


# ---------- normalizar_titulo ----------

@pytest.mark.parametrize("titulo, esperado", [
    ("Cien años de soledad", "cien anos de soledad"),
    ("Fantastic Mr. Fox", "fantastic mr fox"),
    ("  El   Aleph  ", "el aleph"),
    ("¿Quién?", "quien"),
    (None, ""),
    ("...", ""),
])
def test_normalizar_titulo(titulo, esperado):
    assert normalizar_titulo(titulo) == esperado


# ---------- COINCIDE ----------

@pytest.mark.parametrize("catalogo, fuente", [
    ("Fantastic Mr. Fox", "Fantastic Mr. Fox"),
    ("Fantastic Mr Fox", "Fantastic Mr. Fox"),
    ("El Aleph", "El Aleph"),
    ("Cien años de soledad", "Cien anos de soledad"),
    ("EL ALEPH", "el aleph"),
])
def test_coincide(catalogo, fuente):
    resultado = comparar_titulo(catalogo, fuente)

    assert resultado["resultado"] == "COINCIDE"
    assert resultado["similitud"] == 1.0


# ---------- POSIBLE COINCIDENCIA (error de escritura) ----------

def test_un_error_de_tipeo_es_posible_coincidencia():
    resultado = comparar_titulo("Fantastic Mr. Foz", "Fantastic Mr. Fox")

    assert resultado["resultado"] == "POSIBLE COINCIDENCIA"
    assert resultado["similitud"] == pytest.approx(0.9375)


# ---------- POSIBLE VARIANTE (un título contenido en el otro) ----------

@pytest.mark.parametrize("catalogo, fuente", [
    ("Don Quijote", "Don Quijote de la Mancha"),
    ("Don Quijote de la Mancha", "Don Quijote"),
    ("Manual de economía", "Manual de economía política"),
    ("Harry Potter", "Harry Potter y la piedra filosofal"),
])
def test_posible_variante(catalogo, fuente):
    resultado = comparar_titulo(catalogo, fuente)

    assert resultado["resultado"] == "POSIBLE VARIANTE"
    assert resultado["similitud"] < 0.85


# ---------- NO COINCIDE ----------

@pytest.mark.parametrize("catalogo, fuente", [
    ("El Aleph", "Rayuela"),
    ("El amor en los tiempos del cólera", "El amor en los tiempos modernos"),
    ("Historia de la Argentina", "Historia de la literatura argentina"),
    ("La casa de los espíritus", "La casa de Bernarda Alba"),
    ("Cien años de soledad", "Cien años de silencio"),
])
def test_titulos_distintos_no_coinciden(catalogo, fuente):
    resultado = comparar_titulo(catalogo, fuente)

    assert resultado["resultado"] == "NO COINCIDE"
    assert resultado["similitud"] < 0.85


def test_similitud_de_titulos_sin_relacion():
    assert comparar_titulo("El Aleph", "Rayuela")["similitud"] == pytest.approx(0.4)


# ---------- NO DISPONIBLE ----------

@pytest.mark.parametrize("catalogo, fuente", [
    ("", "El Aleph"),
    (None, "El Aleph"),
    ("El Aleph", ""),
    ("El Aleph", None),
    ("", ""),
    (None, None),
    ("   ", "El Aleph"),
    ("...", "El Aleph"),
])
def test_datos_faltantes_son_no_disponible(catalogo, fuente):
    resultado = comparar_titulo(catalogo, fuente)

    assert resultado["resultado"] == "NO DISPONIBLE"
    assert resultado["similitud"] is None


# ---------- Estructura del resultado ----------

def test_el_resultado_conserva_los_originales_y_agrega_los_normalizados():
    resultado = comparar_titulo("Fantastic Mr. Foz", "Fantastic Mr. Fox")

    assert resultado["titulo_catalogo"] == "Fantastic Mr. Foz"
    assert resultado["titulo_fuente"] == "Fantastic Mr. Fox"
    assert resultado["catalogo_normalizado"] == "fantastic mr foz"
    assert resultado["fuente_normalizada"] == "fantastic mr fox"