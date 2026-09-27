# modulos/cargadores/validar_contenido.py

import re


# ----------------------------------------------------
# NORMALIZACIÓN
# ----------------------------------------------------

def normalizar_identificador(valor):
    """
    Convierte el valor a texto y elimina espacios y guiones.
    No modifica el valor original.
    """

    if valor is None:
        return ""

    valor = str(valor).strip()

    valor = valor.replace("-", "")
    valor = valor.replace(" ", "")

    return valor.upper()


# ----------------------------------------------------
# ISBN-10
# ----------------------------------------------------

def es_isbn10(valor):
    """
    Comprueba si un valor tiene formato ISBN-10
    y verifica su dígito de control.
    """

    isbn = normalizar_identificador(valor)

    if len(isbn) != 10:
        return False

    if not re.fullmatch(r"\d{9}[\dX]", isbn):
        return False

    suma = 0

    for posicion, caracter in enumerate(isbn):
        if caracter == "X":
            numero = 10
        else:
            numero = int(caracter)

        suma += (10 - posicion) * numero

    return suma % 11 == 0


# ----------------------------------------------------
# ISBN-13
# ----------------------------------------------------

def es_isbn13(valor):
    """
    Comprueba si un valor tiene formato ISBN-13
    y verifica su dígito de control.
    """

    isbn = normalizar_identificador(valor)

    if len(isbn) != 13:
        return False

    if not isbn.isdigit():
        return False

    suma = 0

    for posicion, caracter in enumerate(isbn[:12]):
        numero = int(caracter)

        if posicion % 2 == 0:
            suma += numero
        else:
            suma += numero * 3

    digito_control = (10 - (suma % 10)) % 10

    return digito_control == int(isbn[-1])


# ----------------------------------------------------
# ISSN
# ----------------------------------------------------

def es_issn(valor):
    """
    Comprueba si un valor tiene formato ISSN
    y verifica su dígito de control.
    """

    issn = normalizar_identificador(valor)

    if len(issn) != 8:
        return False

    if not re.fullmatch(r"\d{7}[\dX]", issn):
        return False

    suma = 0

    for posicion, caracter in enumerate(issn):
        if caracter == "X":
            numero = 10
        else:
            numero = int(caracter)

        suma += (8 - posicion) * numero

    return suma % 11 == 0


# ----------------------------------------------------
# CLASIFICACIÓN
# ----------------------------------------------------

def clasificar_identificador(valor):

    if valor is None:
        return "VACIO"

    texto = str(valor).strip()

    if texto == "":
        return "VACIO"

    normalizado = normalizar_identificador(texto)

    # ------------------------------------------------
    # ISBN-13
    # ------------------------------------------------

    if len(normalizado) == 13 and normalizado.isdigit():

        if es_isbn13(normalizado):
            return "ISBN-13"

        return "ISBN-13 INVÁLIDO"

    # ------------------------------------------------
    # ISBN-10
    # ------------------------------------------------

    if (
        len(normalizado) == 10
        and re.fullmatch(r"\d{9}[\dX]", normalizado)
    ):

        if es_isbn10(normalizado):
            return "ISBN-10"

        return "ISBN-10 INVÁLIDO"

    # ------------------------------------------------
    # ISSN
    # ------------------------------------------------

    if (
        len(normalizado) == 8
        and re.fullmatch(r"\d{7}[\dX]", normalizado)
    ):

        if es_issn(normalizado):
            return "ISSN"

        return "ISSN INVÁLIDO"

    # ------------------------------------------------
    # OTROS
    # ------------------------------------------------

    return "NO IDENTIFICADO"