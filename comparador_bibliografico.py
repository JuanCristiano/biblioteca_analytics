import re

from normalizacion import normalizar_texto, normalizar_autor


def textos_coinciden(valor_catalogo, valores_externos):
    """
    Determina si un valor del catálogo coincide con alguno
    de los valores proporcionados por la fuente externa.

    Utiliza normalización general de texto.
    """

    catalogo = normalizar_texto(valor_catalogo)

    if not catalogo:
        return None

    if not valores_externos:
        return None

    for valor_externo in valores_externos:

        externo = normalizar_texto(valor_externo)

        if catalogo == externo:
            return True

    return False


def autores_coinciden(valor_catalogo, valores_externos):
    """
    Determina si un autor del catálogo coincide con alguno
    de los autores proporcionados por la fuente externa.

    Utiliza normalización específica para nombres de autores,
    permitiendo diferentes formas de representación.

    Ejemplo:

    Gabriel García Márquez
    García Márquez, Gabriel

    se consideran equivalentes.
    """

    autor_catalogo = normalizar_autor(valor_catalogo)

    if not autor_catalogo:
        return None

    if not valores_externos:
        return None

    for autor_externo in valores_externos:

        autor_externo_normalizado = normalizar_autor(
            autor_externo
        )

        if autor_catalogo == autor_externo_normalizado:
            return True

    return False


def comparar_registro(registro_catalogo, registro_externo):
    """
    Compara un registro bibliográfico del catálogo contra
    los datos obtenidos de una fuente externa.

    No modifica ningún registro del catálogo.

    Devuelve un resultado de comparación por campo y
    una conclusión general.
    """

    resultado = {
        "isbn": None,
        "titulo": None,
        "autor": None,
        "editorial": None,
        "resultado": None
    }

    # ----------------------------------------------------
    # ISBN
    # ----------------------------------------------------

    isbn_catalogo = registro_catalogo.get("isbn")
    isbn_externo = registro_externo.get("isbn")

    if isbn_catalogo and isbn_externo:

        isbn_catalogo = re.sub(
            r"[^0-9Xx]",
            "",
            str(isbn_catalogo)
        ).upper()

        isbn_externo = re.sub(
            r"[^0-9Xx]",
            "",
            str(isbn_externo)
        ).upper()

        resultado["isbn"] = (
            isbn_catalogo == isbn_externo
        )

    # ----------------------------------------------------
    # TÍTULO
    # ----------------------------------------------------

    resultado["titulo"] = textos_coinciden(
        registro_catalogo.get("titulo"),
        [registro_externo.get("titulo")]
        if registro_externo.get("titulo")
        else []
    )

    # ----------------------------------------------------
    # AUTOR
    # ----------------------------------------------------

    resultado["autor"] = autores_coinciden(
        registro_catalogo.get("autor"),
        registro_externo.get("autores", [])
    )

    # ----------------------------------------------------
    # EDITORIAL
    # ----------------------------------------------------

    resultado["editorial"] = textos_coinciden(
        registro_catalogo.get("editorial"),
        registro_externo.get("editoriales", [])
    )

    # ----------------------------------------------------
    # RESULTADO GENERAL
    # ----------------------------------------------------

    campos_comparables = [
        resultado["isbn"],
        resultado["titulo"],
        resultado["autor"],
        resultado["editorial"]
    ]

    coincidencias = [
        valor
        for valor in campos_comparables
        if valor is True
    ]

    discrepancias = [
        valor
        for valor in campos_comparables
        if valor is False
    ]

    campos_sin_datos = [
        valor
        for valor in campos_comparables
        if valor is None
    ]

    if discrepancias:

        resultado["resultado"] = "REVISAR"

    elif coincidencias and not campos_sin_datos:

        resultado["resultado"] = "COINCIDE"

    elif coincidencias:

        resultado["resultado"] = "COINCIDE PARCIALMENTE"

    else:

        resultado["resultado"] = "SIN DATOS PARA COMPARAR"

    return resultado