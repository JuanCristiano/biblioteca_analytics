# modulos/cargadores/evaluar_confianza.py

from difflib import SequenceMatcher
import unicodedata


# ============================================================
# EQUIVALENCIAS CONOCIDAS
# ============================================================

EQUIVALENCIAS_CONOCIDAS = {

    "Código": "001",
    "Título principal": "titulo",
    "Responsable": "autor",
    "ISBN-13": "isbn",
    "Publisher": "editorial",
    "Año publicación": "anio",
    "Ubicación": "ubicacion",
    "Código de barras": "codigo_barras",
    "Tipo de material": "tipo_material"

}


# ============================================================
# CAMPOS ESTÁNDAR
#
# Estos son nombres que el sistema reconoce directamente
# como pertenecientes al modelo estándar.
# ============================================================

CAMPOS_ESTANDAR = {

    "titulo",
    "autor",
    "isbn",
    "editorial",
    "anio",
    "ubicacion",
    "codigo_barras",
    "tipo_material",
    "materia"

}


# ============================================================
# SINÓNIMOS Y VARIANTES CONOCIDAS
#
# No incluimos errores de tipeo deliberados.
# Los errores serán detectados mediante similitud.
# ============================================================

SINONIMOS = {

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    "nombre del libro": "titulo",
    "titulo del libro": "titulo",
    "título del libro": "titulo",
    "titulo": "titulo",
    "título": "titulo",
    "nombre titulo": "titulo",
    "nombre título": "titulo",
    "titulo principal": "titulo",
    "título principal": "titulo",
    "titulo de la obra": "titulo",
    "título de la obra": "titulo",
    "obra": "titulo",

    # --------------------------------------------------------
    # AUTOR
    # --------------------------------------------------------

    "autor": "autor",
    "autores": "autor",
    "autor principal": "autor",
    "nombre del autor": "autor",
    "nombre autor": "autor",
    "escritor": "autor",
    "escritora": "autor",
    "autores principales": "autor",
    "autoría": "autor",
    "autoría principal": "autor",

    # --------------------------------------------------------
    # EDITORIAL
    # --------------------------------------------------------

    "editor": "editorial",
    "editorial": "editorial",
    "editoriales": "editorial",
    "casa editora": "editorial",
    "casa editorial": "editorial",
    "publisher": "editorial",
    "publisher name": "editorial",

    # --------------------------------------------------------
    # ISBN
    # --------------------------------------------------------

    "isbn": "isbn",
    "isbn 10": "isbn",
    "isbn 10": "isbn",
    "isbn10": "isbn",
    "isbn 13": "isbn",
    "isbn13": "isbn",
    "isbn-10": "isbn",
    "isbn-13": "isbn",
    "numero isbn": "isbn",
    "número isbn": "isbn",

    # --------------------------------------------------------
    # AÑO
    # --------------------------------------------------------

    "año": "anio",
    "ano": "anio",
    "anio": "anio",
    "año publicación": "anio",
    "año de publicación": "anio",
    "ano de publicacion": "anio",
    "anio de publicacion": "anio",
    "fecha de publicación": "anio",
    "fecha publicacion": "anio",
    "fecha de edicion": "anio",
    "año de edición": "anio",
    "anio de edicion": "anio",

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    "ubicacion": "ubicacion",
    "ubicación": "ubicacion",
    "localizacion": "ubicacion",
    "localización": "ubicacion",
    "ubicación física": "ubicacion",
    "ubicacion fisica": "ubicacion",
    "estanteria": "ubicacion",
    "estantería": "ubicacion",
    "signatura topografica": "ubicacion",
    "signatura topográfica": "ubicacion",

    # --------------------------------------------------------
    # CÓDIGO DE BARRAS
    # --------------------------------------------------------

    "codigo de barras": "codigo_barras",
    "código de barras": "codigo_barras",
    "codigo barras": "codigo_barras",
    "código barras": "codigo_barras",
    "barcode": "codigo_barras",
    "bar code": "codigo_barras",

    # --------------------------------------------------------
    # TIPO DE MATERIAL
    # --------------------------------------------------------

    "tipo": "tipo_material",
    "material": "tipo_material",
    "tipo de material": "tipo_material",
    "tipo material": "tipo_material",
    "material bibliografico": "tipo_material",
    "material bibliográfico": "tipo_material",
    "formato": "tipo_material",
    "soporte": "tipo_material",

    # --------------------------------------------------------
    # MATERIA / TEMÁTICA
    # --------------------------------------------------------

    "materia": "materia",
    "materias": "materia",
    "asignatura": "materia",
    "asignaturas": "materia",
    "tema": "materia",
    "temas": "materia",
    "area tematica": "materia",
    "área temática": "materia",
    "tema principal": "materia",
    "temática": "materia",
    "tematica": "materia",
    "materia bibliografica": "materia",
    "materia bibliográfica": "materia"

}


# ============================================================
# TÉRMINOS INCOMPATIBLES
#
# Sirven para evitar falsos positivos producidos por
# similitud de texto.
# ============================================================

TERMINOS_INCOMPATIBLES = {

    "isbn": {
        "issn",
        "issn 10",
        "issn 13",
        "issn10",
        "issn13"
    },

    "autor": {
        "autoridad",
        "autorizacion",
        "autorización"
    }

}


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar_nombre_columna(nombre):

    nombre = str(nombre)

    nombre = nombre.strip()

    nombre = nombre.lower()

    # Eliminar tildes para comparar variaciones superficiales.

    nombre = unicodedata.normalize(
        "NFKD",
        nombre
    )

    nombre = "".join(
        caracter
        for caracter in nombre
        if not unicodedata.combining(caracter)
    )

    # Unificar separadores.

    nombre = nombre.replace("-", " ")
    nombre = nombre.replace("_", " ")

    # Eliminar espacios duplicados.

    nombre = " ".join(
        nombre.split()
    )

    return nombre


# ============================================================
# SIMILITUD
# ============================================================

def calcular_similitud(texto1, texto2):

    return SequenceMatcher(
        None,
        normalizar_nombre_columna(texto1),
        normalizar_nombre_columna(texto2)
    ).ratio()


# ============================================================
# CONSTRUIR UNIVERSO DE CANDIDATOS
# ============================================================

def construir_candidatos():

    candidatos = {}

    # --------------------------------------------------------
    # Campos estándar
    # --------------------------------------------------------

    for campo in CAMPOS_ESTANDAR:

        candidatos.setdefault(
            campo,
            set()
        )

        candidatos[campo].add(
            campo
        )

    # --------------------------------------------------------
    # Equivalencias conocidas
    # --------------------------------------------------------

    for columna, campo in EQUIVALENCIAS_CONOCIDAS.items():

        candidatos.setdefault(
            campo,
            set()
        )

        candidatos[campo].add(
            columna
        )

    # --------------------------------------------------------
    # Sinónimos
    # --------------------------------------------------------

    for sinonimo, campo in SINONIMOS.items():

        candidatos.setdefault(
            campo,
            set()
        )

        candidatos[campo].add(
            sinonimo
        )

    return candidatos


# ============================================================
# VERIFICAR SI EXISTE UNA INCOMPATIBILIDAD
# ============================================================

def es_incompatible(
    columna_original,
    campo_estandar
):

    columna_normalizada = (
        normalizar_nombre_columna(
            columna_original
        )
    )

    incompatibles = TERMINOS_INCOMPATIBLES.get(
        campo_estandar,
        set()
    )

    return (
        columna_normalizada
        in {
            normalizar_nombre_columna(valor)
            for valor in incompatibles
        }
    )


# ============================================================
# BUSCAR MEJOR COINCIDENCIA
# ============================================================

def buscar_mejor_coincidencia(
    columna_original,
    campo_estandar
):

    candidatos = construir_candidatos()

    candidatos_campo = candidatos.get(
        campo_estandar,
        set()
    )

    mejor_coincidencia = None
    mejor_similitud = 0

    for candidato in candidatos_campo:

        similitud = calcular_similitud(
            columna_original,
            candidato
        )

        if similitud > mejor_similitud:

            mejor_similitud = similitud
            mejor_coincidencia = candidato

    return (
        mejor_coincidencia,
        mejor_similitud
    )


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def evaluar_mapeo(mapeo):

    resultados = []

    equivalencia_normalizada = {

        normalizar_nombre_columna(clave): valor

        for clave, valor
        in EQUIVALENCIAS_CONOCIDAS.items()

    }

    sinonimos_normalizados = {

        normalizar_nombre_columna(clave): valor

        for clave, valor
        in SINONIMOS.items()

    }


    for columna_original, campo_estandar in mapeo.items():

        nombre_normalizado = (
            normalizar_nombre_columna(
                columna_original
            )
        )
        # ----------------------------------------------------
        # NIVEL 0 — NOMBRE ESTÁNDAR EXACTO
        # ----------------------------------------------------

        if (
            nombre_normalizado == campo_estandar
            and campo_estandar in CAMPOS_ESTANDAR
        ):
            confianza = "ALTA"
            motivo = "nombre estándar exacto"


        # ----------------------------------------------------
        # NIVEL 1 — EQUIVALENCIA CONOCIDA
        # ----------------------------------------------------

        elif (
            nombre_normalizado in equivalencia_normalizada
            and equivalencia_normalizada[
                nombre_normalizado
            ] == campo_estandar
        ):
            confianza = "ALTA"
            motivo = "equivalencia conocida"

            
        # ----------------------------------------------------
        # NIVEL 2 — SINÓNIMO / VARIANTE CONOCIDA
        # ----------------------------------------------------

        elif (
            nombre_normalizado
            in sinonimos_normalizados

            and

            sinonimos_normalizados[
                nombre_normalizado
            ]
            == campo_estandar
        ):

            confianza = "MEDIA"

            motivo = (
                "sinónimo o variante conocida"
            )


        # ----------------------------------------------------
        # NIVEL 3 — TÉRMINO INCOMPATIBLE
        # ----------------------------------------------------

        elif es_incompatible(
            columna_original,
            campo_estandar
        ):

            confianza = "BAJA"

            motivo = (
                "término incompatible con "
                "el campo estándar"
            )


        # ----------------------------------------------------
        # NIVEL 4 — SIMILITUD
        # ----------------------------------------------------

        else:

            (
                columna_parecida,
                similitud
            ) = buscar_mejor_coincidencia(
                columna_original,
                campo_estandar
            )


            if (
                columna_parecida is not None
                and
                similitud >= 0.75
            ):

                confianza = "MEDIA"

                motivo = (
                    "posible error de escritura; "
                    f"similar a '{columna_parecida}' "
                    f"({similitud:.0%})"
                )


            # ------------------------------------------------
            # NIVEL 5 — SIN CORRESPONDENCIA
            # ------------------------------------------------

            else:

                confianza = "BAJA"

                motivo = (
                    "sin correspondencia confiable"
                )


        resultados.append({

            "columna_original": columna_original,
            "campo_estandar": campo_estandar,
            "confianza": confianza,
            "motivo": motivo

        })


    return resultados
