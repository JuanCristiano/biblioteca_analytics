from .reglas.validar_titulo import validar_titulo
from .reglas.validar_isbn import validar_isbn
from .reglas.detectar_duplicados import detectar_isbn_duplicados
from .reglas.validar_autor_principal import validar_autor_principal
from .reglas.validar_publicacion import validar_publicacion
from .reglas.validar_descripcion_fisica import validar_descripcion_fisica

from .reglas.validar_anio_publicacion import validar_anio_publicacion
from .reglas.validar_extension import validar_extension
from .reglas.validar_enlace import validar_enlace
from .reglas.validar_subtitulo import validar_subtitulo

from modulos.comparacion.comparar_autores import comparar_multiples_autores


# ====================================================
# COMPARACIÓN DE AUTORES
# ====================================================

def validar_autor_con_fuente(
    registro,
    fuente_autores
):
    """
    Compara el autor del registro del catálogo
    con el autor correspondiente de una fuente externa.

    La comparación solamente se ejecuta si existe
    una fuente externa.

    No modifica el registro original.
    """

    errores = []

    if fuente_autores is None:
        return errores

    identificador = registro.get("001", "")

    autor_fuente = fuente_autores.get(
        identificador
    )

    # ------------------------------------------------
    # EXTRAER AUTOR DEL CATÁLOGO
    # ------------------------------------------------

    autores_catalogo = []

    for campo in ["100", "110", "111"]:

        valores = registro.get(campo)

        if not valores:
            continue

        for valor in valores:

            subcampos = valor.get(
                "subcampos",
                {}
            )

            autor = subcampos.get(
                "a",
                ""
            )

            if autor:
                autores_catalogo.append(
                    autor
                )

    # ------------------------------------------------
    # SI NO HAY DATOS PARA COMPARAR
    # ------------------------------------------------

    if not autores_catalogo and not autor_fuente:
        return errores

    autores_catalogo_texto = "; ".join(
        autores_catalogo
    )

    # ------------------------------------------------
    # COMPARAR
    # ------------------------------------------------

    comparacion = comparar_multiples_autores(
        autores_catalogo_texto,
        autor_fuente
    )

    resultado = comparacion["resultado"]
    motivo = comparacion["motivo"]

    # ------------------------------------------------
    # COINCIDE
    # ------------------------------------------------

    if resultado == "COINCIDE":
        return errores

    # ------------------------------------------------
    # POSIBLE COINCIDENCIA
    # ------------------------------------------------

    if resultado == "POSIBLE COINCIDENCIA":

        errores.append({
            "registro": identificador,
            "campo": "100/110/111",
            "subcampo": "a",
            "regla": "AUTOR-001",
            "nivel": "ADVERTENCIA",
            "problema": (
                "El autor del catálogo presenta "
                "una posible variante respecto "
                "de la fuente externa"
            ),
            "sugerencia": (
                "Revisar manualmente la forma "
                "del nombre del autor."
            )
        })

        return errores

    # ------------------------------------------------
    # REVISAR
    # ------------------------------------------------

    if resultado == "REVISAR":

        if motivo == "AUTOR_FALTANTE":

            problema = (
                "El catálogo contiene un autor "
                "que no aparece en la fuente externa"
            )

            sugerencia = (
                "Revisar si el autor debe conservarse "
                "o si falta información en la fuente."
            )

        elif motivo == "AUTOR_ADICIONAL":

            problema = (
                "La fuente externa contiene un autor "
                "que no aparece en el catálogo"
            )

            sugerencia = (
                "Revisar si corresponde incorporar "
                "el autor al registro."
            )

        elif motivo == "DIFERENCIA_EN_AUTORES":

            problema = (
                "Existen diferencias entre los autores "
                "del catálogo y los de la fuente externa"
            )

            sugerencia = (
                "Comparar manualmente los autores "
                "y determinar la forma bibliográficamente correcta."
            )

        else:

            problema = (
                "No fue posible establecer una "
                "coincidencia confiable entre los autores"
            )

            sugerencia = (
                "Revisar manualmente los datos de autor."
            )

        errores.append({
            "registro": identificador,
            "campo": "100/110/111",
            "subcampo": "a",
            "regla": "AUTOR-001",
            "nivel": "ADVERTENCIA",
            "problema": problema,
            "sugerencia": sugerencia
        })

    return errores


# ====================================================
# AUDITORÍA DE UN REGISTRO
# ====================================================

def auditar_registro(
    registro,
    fuente_autores=None
):
    errores = []

    errores.extend(
        validar_titulo(registro)
    )

    errores.extend(
        validar_isbn(registro)
    )

    errores.extend(
        validar_autor_principal(registro)
    )

    errores.extend(
        validar_autor_con_fuente(
            registro,
            fuente_autores
        )
    )

    errores.extend(
        validar_publicacion(registro)
    )

    errores.extend(
        validar_descripcion_fisica(registro)
    )

    errores.extend(
        validar_anio_publicacion(registro)
    )

    errores.extend(
        validar_extension(registro)
    )

    errores.extend(
        validar_enlace(registro)
    )

    errores.extend(
        validar_subtitulo(registro)
    )

    return errores


# ====================================================
# AUDITORÍA DEL CATÁLOGO
# ====================================================

def auditar_catalogo(
    catalogo,
    fuente_autores=None
):
    errores = []

    for registro in catalogo:

        errores.extend(
            auditar_registro(
                registro,
                fuente_autores
            )
        )

    errores.extend(
        detectar_isbn_duplicados(
            catalogo
        )
    )

    return errores
