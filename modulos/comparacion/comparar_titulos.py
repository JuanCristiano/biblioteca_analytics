import re
import unicodedata
from difflib import SequenceMatcher


# ----------------------------------------------------
# NORMALIZACIÓN DE TÍTULOS
# ----------------------------------------------------

def normalizar_titulo(titulo):
    """
    Normaliza un título únicamente para realizar comparaciones.

    No modifica el valor original del catálogo.

    La normalización:
    - convierte a minúsculas
    - elimina tildes
    - reemplaza signos de puntuación
    - unifica espacios
    """

    if titulo is None:
        return ""

    titulo = str(titulo).strip().lower()

    # Eliminar tildes y otros signos diacríticos
    titulo = unicodedata.normalize("NFD", titulo)

    titulo = "".join(
        caracter
        for caracter in titulo
        if unicodedata.category(caracter) != "Mn"
    )

    # Reemplazar signos de puntuación por espacios
    titulo = re.sub(r"[^\w\s]", " ", titulo)

    # Unificar espacios
    titulo = re.sub(r"\s+", " ", titulo)

    return titulo.strip()


# ----------------------------------------------------
# COMPARACIÓN DE TÍTULOS
# ----------------------------------------------------

def comparar_titulo(titulo_catalogo, titulo_fuente):
    """
    Compara un título del catálogo con un título
    proveniente de una fuente externa.

    Devuelve un diccionario con:

    - titulo_catalogo
    - titulo_fuente
    - catalogo_normalizado
    - fuente_normalizada
    - similitud
    - resultado
    """

    catalogo = normalizar_titulo(titulo_catalogo)
    fuente = normalizar_titulo(titulo_fuente)

    # ------------------------------------------------
    # DATOS ORIGINALES
    # ------------------------------------------------

    resultado = {
        "titulo_catalogo": titulo_catalogo,
        "titulo_fuente": titulo_fuente,
        "catalogo_normalizado": catalogo,
        "fuente_normalizada": fuente,
        "similitud": None,
        "resultado": None
    }

    # ------------------------------------------------
    # DATOS FALTANTES
    # ------------------------------------------------

    if not catalogo or not fuente:
        resultado["resultado"] = "NO DISPONIBLE"
        return resultado

    # ------------------------------------------------
    # COINCIDENCIA EXACTA
    # ------------------------------------------------

    if catalogo == fuente:
        resultado["similitud"] = 1.0
        resultado["resultado"] = "COINCIDE"
        return resultado

    # ------------------------------------------------
    # SIMILITUD
    # ------------------------------------------------

    similitud = SequenceMatcher(
        None,
        catalogo,
        fuente
    ).ratio()

    resultado["similitud"] = round(similitud, 4)

    # ------------------------------------------------
    # POSIBLE ERROR DE ESCRITURA
    # ------------------------------------------------

    if similitud >= 0.85:
        resultado["resultado"] = "POSIBLE COINCIDENCIA"
        return resultado

    # ------------------------------------------------
    # POSIBLE VARIANTE
    # ------------------------------------------------

    if catalogo in fuente or fuente in catalogo:
        resultado["resultado"] = "POSIBLE VARIANTE"
        return resultado

    # ------------------------------------------------
    # DIFERENCIA IMPORTANTE
    # ------------------------------------------------

    resultado["resultado"] = "NO COINCIDE"

    return resultado