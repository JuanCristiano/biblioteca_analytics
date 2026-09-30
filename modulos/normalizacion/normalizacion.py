import re
import unicodedata


def normalizar_texto(valor):
    """
    Normaliza un texto para poder compararlo.

    - Convierte a minúsculas.
    - Elimina tildes.
    - Reemplaza signos de puntuación.
    - Reduce espacios múltiples.
    """

    if valor is None:
        return ""

    valor = str(valor).strip().lower()

    valor = unicodedata.normalize("NFD", valor)

    valor = "".join(
        caracter
        for caracter in valor
        if unicodedata.category(caracter) != "Mn"
    )

    valor = re.sub(r"[^a-z0-9]+", " ", valor)
    valor = re.sub(r"\s+", " ", valor).strip()

    return valor


def normalizar_autor(valor):
    """
    Normaliza un nombre de autor.

    Permite comparar distintas formas de escritura,
    incluyendo:

    Gabriel García Márquez
    García Márquez, Gabriel
    """

    autor = normalizar_texto(valor)

    if not autor:
        return ""

    partes = autor.split()

    # Detectar formato:
    # apellido(s), nombre(s)
    if "," in str(valor):

        original = str(valor).strip()

        apellido, nombre = original.split(",", 1)

        apellido = normalizar_texto(apellido)
        nombre = normalizar_texto(nombre)

        autor = f"{nombre} {apellido}".strip()

    return autor