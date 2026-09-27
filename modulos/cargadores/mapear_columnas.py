import unicodedata


MAPEO_COLUMNAS = {
    # Identificador
    "001": "001",
    "id": "001",
    "codigo": "001",
    "codigo_registro": "001",
    "id_registro": "001",

    # Título
    "titulo": "titulo",
    "titulo_principal": "titulo",
    "titulo_obra": "titulo",
    "title": "titulo",

    # Autor
    "autor": "autor",
    "autor_principal": "autor",
    "responsable": "autor",
    "author": "autor",

    # ISBN
    "isbn": "isbn",
    "isbn13": "isbn",
    "isbn_13": "isbn",

    # Editorial
    "editorial": "editorial",
    "editor": "editorial",
    "publisher": "editorial",

    # Año
    "anio": "anio",
    "ano": "anio",
    "anio_publicacion": "anio",
    "ano_publicacion": "anio",
    "year": "anio",

    # Ubicación
    "ubicacion": "ubicacion",
    "ubicacion_fisica": "ubicacion",
    "localizacion": "ubicacion",
    "location": "ubicacion",

    # Código de barras
    "codigo_de_barras": "codigo_barras",
    "codigo_barras": "codigo_barras",
    "barcode": "codigo_barras",
    "bar_code": "codigo_barras",

    # Tipo de material
    "tipo_de_material": "tipo_material",
    "tipo_material": "tipo_material",
    "material": "tipo_material",
    "item_type": "tipo_material",
}


def quitar_acentos(texto):

    # Para nombres de columnas,
    # tratamos la ñ como n.
    texto = texto.replace(
        "ñ",
        "n"
    )

    texto = texto.replace(
        "Ñ",
        "N"
    )

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


def normalizar_nombre_columna(nombre):

    nombre = nombre.strip().lower()

    nombre = quitar_acentos(
        nombre
    )

    nombre = (
        nombre
        .replace("-", "_")
        .replace(" ", "_")
    )

    return nombre


def mapear_columna(nombre):

    nombre_normalizado = (
        normalizar_nombre_columna(
            nombre
        )
    )

    return MAPEO_COLUMNAS.get(
        nombre_normalizado
    )