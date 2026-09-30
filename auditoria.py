import re

from modulos.comparacion.comparador_bibliografico import comparar_registro
from fuentes_bibliograficas import consultar_openlibrary


def normalizar_isbn(valor):
    """
    Convierte un ISBN a un formato comparable.

    Elimina guiones y espacios.
    Conserva los números y la X.
    """

    if valor is None:
        return ""

    valor = str(valor).strip()

    valor = re.sub(
        r"[^0-9Xx]",
        "",
        valor
    )

    return valor.upper()


def auditar_registros(registros_catalogo):
    """
    Audita una colección de registros bibliográficos
    consultando Open Library mediante el ISBN.

    No modifica los registros originales.
    """

    resultados = []

    for registro_catalogo in registros_catalogo:

        isbn_original = registro_catalogo.get("isbn")

        isbn = normalizar_isbn(isbn_original)

        # ----------------------------------------------------
        # SIN ISBN
        # ----------------------------------------------------

        if not isbn:

            resultado = {
                "isbn": None,
                "titulo": None,
                "autor": None,
                "editorial": None,
                "resultado": "SIN ISBN"
            }

        else:

            # ------------------------------------------------
            # CONSULTAR FUENTE EXTERNA
            # ------------------------------------------------

            registro_externo = consultar_openlibrary(isbn)

            # -----------------------------------------------
            # SIN FUENTE EXTERNA
            # -----------------------------------------------

            if not registro_externo:

                resultado = {
                    "isbn": None,
                    "titulo": None,
                    "autor": None,
                    "editorial": None,
                    "resultado": "SIN FUENTE EXTERNA"
                }

            elif not registro_externo.get("encontrado"):

                resultado = {
                    "isbn": None,
                    "titulo": None,
                    "autor": None,
                    "editorial": None,
                    "resultado": "NO ENCONTRADO"
                }

            # -----------------------------------------------
            # COMPARAR
            # -----------------------------------------------

            else:

                resultado = comparar_registro(
                    registro_catalogo,
                    registro_externo
                )

        # ----------------------------------------------------
        # GUARDAR RESULTADO
        # ----------------------------------------------------

        resultados.append({
            "registro_catalogo": registro_catalogo,
            "resultado": resultado
        })

    return resultados