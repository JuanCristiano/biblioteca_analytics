import re
import unicodedata


def normalizar_texto(valor):
    """
    Normaliza un texto para poder comparar su contenido.

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


def distancia_levenshtein(texto1, texto2):
    """
    Calcula la distancia de Levenshtein entre dos textos.

    La distancia representa la cantidad mínima de operaciones
    necesarias para transformar un texto en otro.
    """

    texto1 = normalizar_texto(texto1)
    texto2 = normalizar_texto(texto2)

    if texto1 == texto2:
        return 0

    if not texto1:
        return len(texto2)

    if not texto2:
        return len(texto1)

    anterior = list(range(len(texto2) + 1))

    for i, caracter1 in enumerate(texto1, start=1):

        actual = [i]

        for j, caracter2 in enumerate(texto2, start=1):

            costo = 0 if caracter1 == caracter2 else 1

            actual.append(
                min(
                    actual[-1] + 1,
                    anterior[j] + 1,
                    anterior[j - 1] + costo
                )
            )

        anterior = actual

    return anterior[-1]


def calcular_similitud(texto1, texto2):
    """
    Calcula una similitud entre 0 y 1.

    1.0 = textos idénticos después de normalizar.
    0.0 = textos completamente diferentes.
    """

    texto1 = normalizar_texto(texto1)
    texto2 = normalizar_texto(texto2)

    if not texto1 and not texto2:
        return 1.0

    if not texto1 or not texto2:
        return 0.0

    distancia = distancia_levenshtein(texto1, texto2)

    longitud_maxima = max(len(texto1), len(texto2))

    return 1 - (distancia / longitud_maxima)