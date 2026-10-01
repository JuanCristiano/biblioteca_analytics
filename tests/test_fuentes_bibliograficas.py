import pytest
import requests

import modulos.fuentes.fuentes_bibliograficas as fb
from modulos.fuentes.fuentes_bibliograficas import consultar_google_books, consultar_openlibrary

ISBN = "9780140328721"

FUENTES = [
    (consultar_openlibrary, "Open Library"),
    (consultar_google_books, "Google Books"),
]


# ---------- Red simulada (ningún test usa internet) ----------

class RespuestaFalsa:
    def __init__(self, datos=None, error_http=None, error_json=None):
        self._datos = datos
        self._error_http = error_http
        self._error_json = error_json

    def raise_for_status(self):
        if self._error_http:
            raise self._error_http

    def json(self):
        if self._error_json:
            raise self._error_json
        return self._datos


class RedFalsa:
    def __init__(self):
        self.llamadas = []
        self.respuesta = None
        self.excepcion = None

    def get(self, url, **kwargs):
        self.llamadas.append({"url": url, **kwargs})
        if self.excepcion:
            raise self.excepcion
        return self.respuesta


@pytest.fixture
def red(monkeypatch):
    falsa = RedFalsa()
    monkeypatch.setattr(fb.requests, "get", falsa.get)
    return falsa


def libro_openlibrary():
    return {
        "title": "Fantastic Mr. Fox",
        "authors": [{"name": "Roald Dahl"}, {"name": "Roald Dahl"}, {"name": "Quentin Blake"}],
        "publishers": [{"name": "Puffin"}, {}],
        "publish_date": "1988",
        "identifiers": {"isbn_10": ["0140328726"], "isbn_13": [ISBN]},
        "url": "https://openlibrary.org/books/OL1M/Fantastic_Mr._Fox",
    }


def volumen_google(**cambios):
    info = {
        "title": "Fantastic Mr Fox",
        "authors": ["Roald Dahl"],
        "publisher": "Puffin",
        "publishedDate": "1988",
        "industryIdentifiers": [
            {"type": "ISBN_10", "identifier": "0140328726"},
            {"type": "ISBN_13", "identifier": ISBN},
            {"type": "OTHER", "identifier": "PKEY:123"},
        ],
    }
    info.update(cambios)
    return {"id": "abc123", "volumeInfo": info}


# ---------- Comportamiento común a las dos fuentes ----------

@pytest.mark.parametrize("funcion, fuente", FUENTES)
@pytest.mark.parametrize("isbn", ["", None])
def test_isbn_vacio_no_consulta_internet(red, funcion, fuente, isbn):
    assert funcion(isbn) == {"fuente": fuente, "encontrado": False, "error": "ISBN vacío"}
    assert red.llamadas == []


@pytest.mark.parametrize("funcion, fuente", FUENTES)
def test_timeout(red, funcion, fuente):
    red.excepcion = requests.exceptions.Timeout()

    assert funcion(ISBN) == {
        "fuente": fuente,
        "encontrado": False,
        "error": "Tiempo de espera agotado",
    }


@pytest.mark.parametrize("funcion, fuente", FUENTES)
def test_error_de_conexion(red, funcion, fuente):
    red.excepcion = requests.exceptions.ConnectionError("sin red")

    assert funcion(ISBN) == {
        "fuente": fuente,
        "encontrado": False,
        "error": "Error de conexión: sin red",
    }


@pytest.mark.parametrize("funcion, fuente", FUENTES)
def test_un_error_http_se_informa_como_error_de_conexion(red, funcion, fuente):
    # Es lo que te pasó con el 404: hoy no se distingue de un corte de red.
    red.respuesta = RespuestaFalsa(
        error_http=requests.exceptions.HTTPError("404 Client Error: Not Found")
    )

    resultado = funcion(ISBN)

    assert resultado["encontrado"] is False
    assert resultado["error"] == "Error de conexión: 404 Client Error: Not Found"


@pytest.mark.parametrize("funcion, fuente", FUENTES)
def test_json_invalido(red, funcion, fuente):
    red.respuesta = RespuestaFalsa(error_json=ValueError("no es json"))

    assert funcion(ISBN) == {
        "fuente": fuente,
        "encontrado": False,
        "error": "Respuesta JSON inválida",
    }


# ---------- Open Library ----------

def test_openlibrary_devuelve_los_datos_normalizados(red):
    red.respuesta = RespuestaFalsa({f"ISBN:{ISBN}": libro_openlibrary()})

    assert consultar_openlibrary(ISBN) == {
        "fuente": "Open Library",
        "encontrado": True,
        "isbn": ISBN,
        "titulo": "Fantastic Mr. Fox",
        "autores": ["Roald Dahl", "Quentin Blake"],
        "editoriales": ["Puffin"],
        "fecha_publicacion": "1988",
        "isbn_10": ["0140328726"],
        "isbn_13": [ISBN],
        "openlibrary_url": "https://openlibrary.org/books/OL1M/Fantastic_Mr._Fox",
    }


def test_openlibrary_consulta_con_los_parametros_esperados(red):
    red.respuesta = RespuestaFalsa({})

    consultar_openlibrary(f"  {ISBN}  ")

    assert red.llamadas == [{
        "url": "https://openlibrary.org/api/books",
        "params": {"bibkeys": f"ISBN:{ISBN}", "jscmd": "data", "format": "json"},
        "headers": {"User-Agent": "biblioteca_analytics/1.0"},
        "timeout": 10,
    }]


def test_openlibrary_ignora_los_espacios_alrededor_del_isbn(red):
    red.respuesta = RespuestaFalsa({f"ISBN:{ISBN}": libro_openlibrary()})

    resultado = consultar_openlibrary(f"  {ISBN}  ")

    assert resultado["encontrado"] is True
    assert resultado["isbn"] == ISBN


def test_openlibrary_isbn_no_encontrado(red):
    red.respuesta = RespuestaFalsa({})

    assert consultar_openlibrary(ISBN) == {
        "fuente": "Open Library",
        "encontrado": False,
        "error": "ISBN no encontrado",
    }


def test_openlibrary_con_datos_incompletos_usa_valores_vacios(red):
    red.respuesta = RespuestaFalsa({f"ISBN:{ISBN}": {}})

    assert consultar_openlibrary(ISBN) == {
        "fuente": "Open Library",
        "encontrado": True,
        "isbn": ISBN,
        "titulo": None,
        "autores": [],
        "editoriales": [],
        "fecha_publicacion": None,
        "isbn_10": [],
        "isbn_13": [],
        "openlibrary_url": None,
    }


# ---------- Google Books ----------

def test_google_books_devuelve_los_datos_normalizados(red):
    red.respuesta = RespuestaFalsa({"totalItems": 1, "items": [volumen_google()]})

    assert consultar_google_books(ISBN) == {
        "fuente": "Google Books",
        "encontrado": True,
        "isbn": ISBN,
        "titulo": "Fantastic Mr Fox",
        "autores": ["Roald Dahl"],
        "editoriales": ["Puffin"],
        "fecha_publicacion": "1988",
        "isbn_10": ["0140328726"],
        "isbn_13": [ISBN],
        "google_books_id": "abc123",
    }


def test_google_books_consulta_con_los_parametros_esperados(red):
    red.respuesta = RespuestaFalsa({"totalItems": 0})

    consultar_google_books(f"  {ISBN}  ")

    assert red.llamadas == [{
        "url": "https://www.googleapis.com/books/v1/volumes",
        "params": {"q": f"isbn:{ISBN}", "maxResults": 10},
        "timeout": 10,
    }]


def test_google_books_usa_solo_el_primer_resultado(red):
    segundo = volumen_google(title="Otro libro")
    segundo["id"] = "zzz"
    red.respuesta = RespuestaFalsa({"totalItems": 2, "items": [volumen_google(), segundo]})

    resultado = consultar_google_books(ISBN)

    assert resultado["titulo"] == "Fantastic Mr Fox"
    assert resultado["google_books_id"] == "abc123"


def test_google_books_sin_editorial_devuelve_lista_vacia(red):
    red.respuesta = RespuestaFalsa({"totalItems": 1, "items": [volumen_google(publisher=None)]})

    assert consultar_google_books(ISBN)["editoriales"] == []


@pytest.mark.parametrize("datos", [{"totalItems": 0}, {}])
def test_google_books_isbn_no_encontrado(red, datos):
    red.respuesta = RespuestaFalsa(datos)

    assert consultar_google_books(ISBN) == {
        "fuente": "Google Books",
        "encontrado": False,
        "error": "ISBN no encontrado",
    }


def test_google_books_con_datos_incompletos_usa_valores_vacios(red):
    red.respuesta = RespuestaFalsa({"totalItems": 1, "items": [{"id": "x"}]})

    assert consultar_google_books(ISBN) == {
        "fuente": "Google Books",
        "encontrado": True,
        "isbn": ISBN,
        "titulo": None,
        "autores": [],
        "editoriales": [],
        "fecha_publicacion": None,
        "isbn_10": [],
        "isbn_13": [],
        "google_books_id": "x",
    }


# ---------- Limitación conocida ----------

def test_limitacion_totalitems_sin_items_provoca_un_error_sin_capturar(red):
    red.respuesta = RespuestaFalsa({"totalItems": 1})

    with pytest.raises(KeyError):
        consultar_google_books(ISBN)