import copy

import pytest

import modulos.fuentes.auditoria as modulo_auditoria
from modulos.fuentes.auditoria import auditar_registros, normalizar_isbn

ISBN = "9780140328721"

NO_ENCONTRADO = {"fuente": "Open Library", "encontrado": False, "error": "ISBN no encontrado"}


# ---------- Fuente externa simulada (ningún test usa internet) ----------

class FuenteFalsa:
    def __init__(self):
        self.respuestas = {}
        self.por_defecto = NO_ENCONTRADO
        self.consultas = []

    def __call__(self, isbn):
        self.consultas.append(isbn)
        return self.respuestas.get(isbn, self.por_defecto)


@pytest.fixture
def fuente(monkeypatch):
    falsa = FuenteFalsa()
    monkeypatch.setattr(modulo_auditoria, "consultar_openlibrary", falsa)
    return falsa


def externo(**cambios):
    datos = {
        "fuente": "Open Library",
        "encontrado": True,
        "isbn": ISBN,
        "titulo": "Fantastic Mr Fox",
        "autores": ["Roald Dahl"],
        "editoriales": ["Puffin"],
    }
    datos.update(cambios)
    return datos


def registro(**cambios):
    datos = {
        "isbn": ISBN,
        "titulo": "Fantastic Mr. Fox",
        "autor": "Roald Dahl",
        "editorial": "Puffin",
    }
    datos.update(cambios)
    return datos


def resultado_de(resultados, posicion=0):
    return resultados[posicion]["resultado"]


SIN_DATOS = {"isbn": None, "titulo": None, "autor": None, "editorial": None}


# ---------- normalizar_isbn ----------

@pytest.mark.parametrize("valor, esperado", [
    ("978-0-14-032872-1", "9780140328721"),
    (" 9780140328721 ", "9780140328721"),
    ("ISBN 978-0-14-032872-1", "9780140328721"),
    ("080442957x", "080442957X"),
    (9780140328721, "9780140328721"),
    (None, ""),
    ("", ""),
])
def test_normalizar_isbn(valor, esperado):
    assert normalizar_isbn(valor) == esperado


def test_limitacion_una_x_dentro_de_un_texto_se_toma_como_isbn():
    # Un campo de ISBN con texto libre que contenga una "x" produce un "ISBN" falso.
    assert normalizar_isbn("Excelente") == "X"


# ---------- Registros sin ISBN ----------

@pytest.mark.parametrize("isbn", [None, "", "   ", "sin isbn"])
def test_sin_isbn_no_consulta_la_fuente(fuente, isbn):
    resultados = auditar_registros([registro(isbn=isbn)])

    assert resultado_de(resultados) == {**SIN_DATOS, "resultado": "SIN ISBN"}
    assert fuente.consultas == []


def test_un_registro_sin_la_clave_isbn_es_sin_isbn(fuente):
    resultados = auditar_registros([{"titulo": "Libro sin ISBN"}])

    assert resultado_de(resultados)["resultado"] == "SIN ISBN"
    assert fuente.consultas == []


# ---------- Registros con ISBN ----------

def test_coincide_y_consulta_con_el_isbn_normalizado(fuente):
    fuente.respuestas = {ISBN: externo()}

    resultados = auditar_registros([registro(isbn="978-0-14-032872-1")])

    assert fuente.consultas == [ISBN]
    assert resultado_de(resultados) == {
        "isbn": True,
        "titulo": True,
        "autor": True,
        "editorial": True,
        "resultado": "COINCIDE",
    }


def test_un_titulo_con_error_de_tipeo_pide_revision(fuente):
    fuente.respuestas = {ISBN: externo()}

    resultados = auditar_registros([registro(titulo="Fantastic Mr. Foz")])

    assert resultado_de(resultados) == {
        "isbn": True,
        "titulo": False,
        "autor": True,
        "editorial": True,
        "resultado": "REVISAR",
    }


def test_el_autor_con_formato_apellido_nombre_coincide(fuente):
    fuente.respuestas = {ISBN: externo()}

    resultados = auditar_registros([registro(autor="Dahl, Roald")])

    assert resultado_de(resultados)["autor"] is True
    assert resultado_de(resultados)["resultado"] == "COINCIDE"


def test_isbn_no_encontrado(fuente):
    resultados = auditar_registros([registro(isbn="9999999999999")])

    assert fuente.consultas == ["9999999999999"]
    assert resultado_de(resultados) == {**SIN_DATOS, "resultado": "NO ENCONTRADO"}


@pytest.mark.parametrize("respuesta", [None, {}])
def test_sin_respuesta_de_la_fuente(fuente, respuesta):
    fuente.por_defecto = respuesta

    resultados = auditar_registros([registro()])

    assert resultado_de(resultados) == {**SIN_DATOS, "resultado": "SIN FUENTE EXTERNA"}


# ---------- Lotes de registros ----------

def test_lista_vacia():
    assert auditar_registros([]) == []


def test_un_lote_mixto_conserva_el_orden_de_los_registros(fuente):
    fuente.respuestas = {ISBN: externo()}
    registros = [
        registro(),
        {"isbn": "", "titulo": "Libro sin ISBN"},
        registro(isbn="9999999999999", titulo="Libro inexistente"),
    ]

    resultados = auditar_registros(registros)

    assert [r["resultado"]["resultado"] for r in resultados] == [
        "COINCIDE", "SIN ISBN", "NO ENCONTRADO",
    ]
    assert [r["registro_catalogo"]["titulo"] for r in resultados] == [
        "Fantastic Mr. Fox", "Libro sin ISBN", "Libro inexistente",
    ]


def test_devuelve_el_mismo_registro_del_catalogo_junto_a_su_resultado(fuente):
    original = registro()

    resultados = auditar_registros([original])

    assert set(resultados[0]) == {"registro_catalogo", "resultado"}
    assert resultados[0]["registro_catalogo"] is original


def test_no_modifica_los_registros_originales(fuente):
    fuente.respuestas = {ISBN: externo()}
    registros = [registro(isbn=" 978-0-14-032872-1 "), {"isbn": None, "titulo": "x"}]
    copia = copy.deepcopy(registros)

    auditar_registros(registros)

    assert registros == copia


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

def test_limitacion_un_error_de_conexion_se_informa_como_no_encontrado(fuente):
    # Es lo que pasa hoy con el 404: se confunde una consulta fallida con un ISBN inexistente.
    fuente.por_defecto = {
        "fuente": "Open Library",
        "encontrado": False,
        "error": "Error de conexión: 404 Client Error: Not Found",
    }

    resultados = auditar_registros([registro()])

    assert resultado_de(resultados)["resultado"] == "NO ENCONTRADO"


def test_limitacion_un_isbn_repetido_se_consulta_una_vez_por_registro(fuente):
    fuente.respuestas = {ISBN: externo()}

    auditar_registros([registro(), registro(titulo="Fantastic Mr. Foz"), registro(autor="Dahl, Roald")])

    assert fuente.consultas == [ISBN, ISBN, ISBN]