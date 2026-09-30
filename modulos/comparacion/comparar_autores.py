
import re
import unicodedata
from difflib import SequenceMatcher


# ====================================================
# NORMALIZACIÓN DE AUTORES
# ====================================================

def normalizar_autor(autor):
    """
    Normaliza un nombre de autor únicamente para realizar
    comparaciones.

    No modifica el valor original.

    La normalización:
    - convierte a minúsculas
    - elimina tildes
    - reemplaza puntuación
    - unifica espacios
    """

    if autor is None:
        return ""

    autor = str(autor).strip().lower()

    # Eliminar tildes
    autor = unicodedata.normalize("NFD", autor)

    autor = "".join(
        caracter
        for caracter in autor
        if unicodedata.category(caracter) != "Mn"
    )

    # Reemplazar puntuación por espacios
    autor = re.sub(r"[^\w\s]", " ", autor)

    # Unificar espacios
    autor = re.sub(r"\s+", " ", autor)

    return autor.strip()


# ====================================================
# REORDENAMIENTO DE AUTOR
# ====================================================

def reordenar_autor(autor):
    """
    Detecta el formato:

        Apellido, Nombre

    y lo transforma internamente en:

        Nombre Apellido

    Si no existe coma, conserva el orden original.
    """

    if not autor:
        return ""

    partes = [
        parte.strip()
        for parte in autor.split(",")
    ]

    if len(partes) == 2:

        apellido = partes[0]
        nombre = partes[1]

        return f"{nombre} {apellido}".strip()

    return autor


# ====================================================
# COMPARACIÓN DE UN AUTOR
# ====================================================

def comparar_autor(
    autor_catalogo,
    autor_fuente
):
    """
    Compara un autor del catálogo con un autor
    proveniente de una fuente externa.

    Resultados posibles:

    COINCIDE
    POSIBLE COINCIDENCIA
    NO COINCIDE
    NO DISPONIBLE
    """

    resultado = {
        "autor_catalogo": autor_catalogo,
        "autor_fuente": autor_fuente,
        "catalogo_normalizado": "",
        "fuente_normalizada": "",
        "similitud": None,
        "resultado": None
    }

    # ------------------------------------------------
    # DATOS FALTANTES
    # ------------------------------------------------

    if (
        autor_catalogo is None
        or str(autor_catalogo).strip() == ""
    ):

        resultado["resultado"] = "NO DISPONIBLE"

        return resultado

    if (
        autor_fuente is None
        or str(autor_fuente).strip() == ""
    ):

        resultado["resultado"] = "NO DISPONIBLE"

        return resultado

    # ------------------------------------------------
    # REORDENAR
    # ------------------------------------------------

    catalogo_reordenado = reordenar_autor(
        str(autor_catalogo).strip()
    )

    fuente_reordenada = reordenar_autor(
        str(autor_fuente).strip()
    )

    # ------------------------------------------------
    # NORMALIZAR
    # ------------------------------------------------

    catalogo = normalizar_autor(
        catalogo_reordenado
    )

    fuente = normalizar_autor(
        fuente_reordenada
    )

    resultado["catalogo_normalizado"] = catalogo
    resultado["fuente_normalizada"] = fuente

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

    resultado["similitud"] = round(
        similitud,
        4
    )

    # ------------------------------------------------
    # POSIBLE COINCIDENCIA
    # ------------------------------------------------

    if similitud >= 0.85:

        resultado["resultado"] = (
            "POSIBLE COINCIDENCIA"
        )

        return resultado

    # ------------------------------------------------
    # NO COINCIDE
    # ------------------------------------------------

    resultado["resultado"] = "NO COINCIDE"

    return resultado


# ====================================================
# SEPARAR MÚLTIPLES AUTORES
# ====================================================

def separar_autores(campo):
    """
    Separa un campo que contiene múltiples autores.

    Separadores reconocidos:

    ;
    /
    y

    La función NO modifica los nombres.
    """

    if campo is None:
        return []

    campo = str(campo).strip()

    if not campo:
        return []

    # ------------------------------------------------
    # PUNTO Y COMA
    # ------------------------------------------------

    partes = re.split(
        r"\s*;\s*",
        campo
    )

    resultado = []

    for parte in partes:

        # ------------------------------------------------
        # BARRA
        # ------------------------------------------------

        subpartes = re.split(
            r"\s*/\s*",
            parte
        )

        for subparte in subpartes:

            # ------------------------------------------------
            # "Y"
            # ------------------------------------------------

            autores = re.split(
                r"\s+y\s+",
                subparte,
                flags=re.IGNORECASE
            )

            for autor in autores:

                autor = autor.strip()

                if autor:

                    resultado.append(
                        autor
                    )

    return resultado


# ====================================================
# COMPARACIÓN DE MÚLTIPLES AUTORES
# ====================================================

def comparar_multiples_autores(
    autores_catalogo,
    autores_fuente
):
    """
    Compara conjuntos de autores.

    Analiza:

    - autores coincidentes
    - posibles coincidencias
    - autores faltantes
    - autores adicionales
    - cantidad de autores

    No modifica los datos originales.
    """

    # ------------------------------------------------
    # ESTRUCTURA DEL RESULTADO
    # ------------------------------------------------

    resultado = {
        "autores_catalogo": [],
        "autores_fuente": [],

        "cantidad_catalogo": 0,
        "cantidad_fuente": 0,

        "coincidencias": [],
        "posibles_coincidencias": [],

        "faltantes": [],
        "adicionales": [],

        "resultado": None,
        "motivo": None
    }

    # ------------------------------------------------
    # SEPARAR AUTORES
    # ------------------------------------------------

    lista_catalogo = separar_autores(
        autores_catalogo
    )

    lista_fuente = separar_autores(
        autores_fuente
    )

    # ------------------------------------------------
    # GUARDAR LISTAS
    # ------------------------------------------------

    resultado["autores_catalogo"] = (
        lista_catalogo
    )

    resultado["autores_fuente"] = (
        lista_fuente
    )

    resultado["cantidad_catalogo"] = (
        len(lista_catalogo)
    )

    resultado["cantidad_fuente"] = (
        len(lista_fuente)
    )

    # ------------------------------------------------
    # DATOS FALTANTES
    # ------------------------------------------------

    if (
        not lista_catalogo
        or not lista_fuente
    ):

        resultado["resultado"] = (
            "NO DISPONIBLE"
        )

        resultado["motivo"] = (
            "DATOS_FALTANTES"
        )

        return resultado

    # ------------------------------------------------
    # AUTORES DE LA FUENTE YA UTILIZADOS
    # ------------------------------------------------

    autores_fuente_utilizados = set()

    # ------------------------------------------------
    # COMPARAR CADA AUTOR DEL CATÁLOGO
    # ------------------------------------------------

    for autor_catalogo in lista_catalogo:

        mejor_resultado = None
        mejor_indice = None

        # --------------------------------------------
        # COMPARAR CONTRA CADA AUTOR DE LA FUENTE
        # --------------------------------------------

        for indice_fuente, autor_fuente in enumerate(
            lista_fuente
        ):

            # Ya fue utilizado
            if (
                indice_fuente
                in autores_fuente_utilizados
            ):

                continue

            comparacion = comparar_autor(
                autor_catalogo,
                autor_fuente
            )

            # ----------------------------------------
            # COINCIDENCIA EXACTA
            # ----------------------------------------

            if (
                comparacion["resultado"]
                == "COINCIDE"
            ):

                mejor_resultado = (
                    comparacion
                )

                mejor_indice = (
                    indice_fuente
                )

                break

            # ----------------------------------------
            # POSIBLE COINCIDENCIA
            # ----------------------------------------

            if (
                comparacion["resultado"]
                == "POSIBLE COINCIDENCIA"
            ):

                if (
                    mejor_resultado is None
                    or
                    comparacion["similitud"]
                    >
                    mejor_resultado["similitud"]
                ):

                    mejor_resultado = (
                        comparacion
                    )

                    mejor_indice = (
                        indice_fuente
                    )

        # --------------------------------------------
        # NO ENCONTRAMOS COINCIDENCIA
        # --------------------------------------------

        if mejor_resultado is None:

            resultado["faltantes"].append(
                autor_catalogo
            )

            continue

        # --------------------------------------------
        # MARCAR AUTOR DE FUENTE COMO UTILIZADO
        # --------------------------------------------

        autores_fuente_utilizados.add(
            mejor_indice
        )

        # --------------------------------------------
        # REGISTRO DE LA COMPARACIÓN
        # --------------------------------------------

        registro = {
            "catalogo": autor_catalogo,
            "fuente": lista_fuente[
                mejor_indice
            ],
            "similitud": (
                mejor_resultado[
                    "similitud"
                ]
            ),
            "resultado": (
                mejor_resultado[
                    "resultado"
                ]
            )
        }

        # --------------------------------------------
        # GUARDAR SEGÚN RESULTADO
        # --------------------------------------------

        if (
            mejor_resultado["resultado"]
            == "COINCIDE"
        ):

            resultado["coincidencias"].append(
                registro
            )

        else:

            resultado[
                "posibles_coincidencias"
            ].append(
                registro
            )

    # =================================================
    # BUSCAR AUTORES ADICIONALES
    # =================================================

    for indice_fuente, autor_fuente in enumerate(
        lista_fuente
    ):

        if (
            indice_fuente
            not in autores_fuente_utilizados
        ):

            resultado["adicionales"].append(
                autor_fuente
            )

    # =================================================
    # CANTIDADES
    # =================================================

    total_catalogo = len(
        lista_catalogo
    )

    total_fuente = len(
        lista_fuente
    )

    cantidad_coincidencias = len(
        resultado["coincidencias"]
    )

    cantidad_posibles = len(
        resultado[
            "posibles_coincidencias"
        ]
    )

    cantidad_faltantes = len(
        resultado["faltantes"]
    )

    cantidad_adicionales = len(
        resultado["adicionales"]
    )

    # =================================================
    # RESULTADO: COINCIDE
    # =================================================

    if (
        cantidad_coincidencias
        == total_catalogo
        and
        total_catalogo
        == total_fuente
    ):

        resultado["resultado"] = (
            "COINCIDE"
        )

        resultado["motivo"] = None

        return resultado

    # =================================================
    # RESULTADO: POSIBLE COINCIDENCIA
    # =================================================

    if (
        cantidad_faltantes == 0
        and
        cantidad_adicionales == 0
        and
        cantidad_posibles > 0
    ):

        resultado["resultado"] = (
            "POSIBLE COINCIDENCIA"
        )

        resultado["motivo"] = (
            "POSIBLE_VARIANTE"
        )

        return resultado

    # =================================================
    # RESULTADO: REVISAR
    # =================================================

    resultado["resultado"] = (
        "REVISAR"
    )

    # -----------------------------------------------
    # FALTANTE
    # -----------------------------------------------

    if (
        cantidad_faltantes > 0
        and
        cantidad_adicionales == 0
    ):

        resultado["motivo"] = (
            "AUTOR_FALTANTE"
        )

    # -----------------------------------------------
    # ADICIONAL
    # -----------------------------------------------

    elif (
        cantidad_faltantes == 0
        and
        cantidad_adicionales > 0
    ):

        resultado["motivo"] = (
            "AUTOR_ADICIONAL"
        )

    # -----------------------------------------------
    # DIFERENCIAS EN AMBOS LADOS
    # -----------------------------------------------

    elif (
        cantidad_faltantes > 0
        and
        cantidad_adicionales > 0
    ):

        resultado["motivo"] = (
            "DIFERENCIA_EN_AUTORES"
        )

    # -----------------------------------------------
    # OTRO CASO
    # -----------------------------------------------

    else:

        resultado["motivo"] = (
            "FORMATO_O_COMPARACION_DUDOSA"
        )

    return resultado
