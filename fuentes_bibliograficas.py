import requests


# ----------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------

OPENLIBRARY_URL = "https://openlibrary.org/isbn/{isbn}.json"
GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"


# ----------------------------------------------------
# OPEN LIBRARY
# ----------------------------------------------------

def consultar_openlibrary(isbn):
    """
    Consulta Open Library utilizando un ISBN.

    Devuelve un diccionario normalizado con los principales
    datos bibliográficos encontrados.
    """

    if not isbn:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": "ISBN vacío"
        }

    isbn = str(isbn).strip()

    url = "https://openlibrary.org/api/books"

    parametros = {
        "bibkeys": f"ISBN:{isbn}",
        "jscmd": "data",
        "format": "json"
    }

    headers = {
        "User-Agent": "biblioteca_analytics/1.0"
    }

    try:
        respuesta = requests.get(
            url,
            params=parametros,
            headers=headers,
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        clave = f"ISBN:{isbn}"

        if clave not in datos:
            return {
                "fuente": "Open Library",
                "encontrado": False,
                "error": "ISBN no encontrado"
            }

        libro = datos[clave]

        autores = []

        for autor in libro.get("authors", []):
            nombre = autor.get("name")

            if nombre and nombre not in autores:
                autores.append(nombre)

        editoriales = [
            editorial.get("name")
            for editorial in libro.get("publishers", [])
            if editorial.get("name")
        ]

        identificadores = libro.get(
            "identifiers",
            {}
        )

        return {
            "fuente": "Open Library",
            "encontrado": True,
            "isbn": isbn,
            "titulo": libro.get("title"),
            "autores": autores,
            "editoriales": editoriales,
            "fecha_publicacion": libro.get("publish_date"),
            "isbn_10": identificadores.get("isbn_10", []),
            "isbn_13": identificadores.get("isbn_13", []),
            "openlibrary_url": libro.get("url")
        }

    except requests.exceptions.Timeout:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": "Tiempo de espera agotado"
        }

    except requests.exceptions.RequestException as error:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": f"Error de conexión: {error}"
        }

    except ValueError:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": "Respuesta JSON inválida"
        }
    """
    Consulta Open Library utilizando un ISBN.

    Devuelve un diccionario normalizado con los principales
    datos bibliográficos encontrados.
    """

    if not isbn:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": "ISBN vacío"
        }

    isbn = str(isbn).strip()

    url = OPENLIBRARY_URL.format(isbn=isbn)

    headers = {
        "User-Agent": "biblioteca_analytics/1.0"
    }

    try:
        respuesta = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if respuesta.status_code == 404:
            return {
                "fuente": "Open Library",
                "encontrado": False,
                "error": "ISBN no encontrado"
            }

        respuesta.raise_for_status()

        datos = respuesta.json()

        autores = [
            autor.get("name")
            for autor in datos.get("authors", [])
            if autor.get("name")
        ]

        editoriales = datos.get("publishers", [])

        return {
            "fuente": "Open Library",
            "encontrado": True,
            "isbn": isbn,
            "titulo": datos.get("title"),
            "autores": autores,
            "editoriales": editoriales,
            "fecha_publicacion": datos.get("publish_date"),
            "isbn_10": datos.get("isbn_10", []),
            "isbn_13": datos.get("isbn_13", []),
            "openlibrary_id": datos.get("key")
        }

    except requests.exceptions.Timeout:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": "Tiempo de espera agotado"
        }

    except requests.exceptions.RequestException as error:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": f"Error de conexión: {error}"
        }

    except ValueError:
        return {
            "fuente": "Open Library",
            "encontrado": False,
            "error": "Respuesta JSON inválida"
        }


# ----------------------------------------------------
# GOOGLE BOOKS
# ----------------------------------------------------

def consultar_google_books(isbn):
    """
    Consulta Google Books utilizando un ISBN.

    Devuelve un diccionario normalizado con los principales
    datos bibliográficos encontrados.
    """

    if not isbn:
        return {
            "fuente": "Google Books",
            "encontrado": False,
            "error": "ISBN vacío"
        }

    isbn = str(isbn).strip()

    parametros = {
        "q": f"isbn:{isbn}",
        "maxResults": 10
    }

    try:
        respuesta = requests.get(
            GOOGLE_BOOKS_URL,
            params=parametros,
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        if datos.get("totalItems", 0) == 0:
            return {
                "fuente": "Google Books",
                "encontrado": False,
                "error": "ISBN no encontrado"
            }

        volumen = datos["items"][0]
        volume_info = volumen.get("volumeInfo", {})

        autores = volume_info.get("authors", [])

        identificadores = volume_info.get(
            "industryIdentifiers",
            []
        )

        isbn_10 = []
        isbn_13 = []

        for identificador in identificadores:

            tipo = identificador.get("type")
            valor = identificador.get("identifier")

            if tipo == "ISBN_10":
                isbn_10.append(valor)

            elif tipo == "ISBN_13":
                isbn_13.append(valor)

        return {
            "fuente": "Google Books",
            "encontrado": True,
            "isbn": isbn,
            "titulo": volume_info.get("title"),
            "autores": autores,
            "editoriales": (
                [volume_info["publisher"]]
                if volume_info.get("publisher")
                else []
            ),
            "fecha_publicacion": volume_info.get(
                "publishedDate"
            ),
            "isbn_10": isbn_10,
            "isbn_13": isbn_13,
            "google_books_id": volumen.get("id")
        }

    except requests.exceptions.Timeout:
        return {
            "fuente": "Google Books",
            "encontrado": False,
            "error": "Tiempo de espera agotado"
        }

    except requests.exceptions.RequestException as error:
        return {
            "fuente": "Google Books",
            "encontrado": False,
            "error": f"Error de conexión: {error}"
        }

    except ValueError:
        return {
            "fuente": "Google Books",
            "encontrado": False,
            "error": "Respuesta JSON inválida"
        }