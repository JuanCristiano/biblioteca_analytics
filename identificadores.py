import re


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


def es_isbn_10_valido(valor):
    """
    Verifica si un valor es un ISBN-10 válido.
    """

    isbn = normalizar_identificador(valor)

    if len(isbn) != 10:
        return False

    if not re.fullmatch(r"[0-9]{9}[0-9X]", isbn):
        return False

    suma = 0

    for posicion, caracter in enumerate(isbn, start=1):

        if caracter == "X":
            digito = 10
        else:
            digito = int(caracter)

        suma += posicion * digito

    return suma % 11 == 0


def es_isbn_13_valido(valor):
    """
    Verifica si un valor es un ISBN-13 válido.
    """

    isbn = normalizar_identificador(valor)

    if len(isbn) != 13:
        return False

    if not isbn.isdigit():
        return False

    suma = 0

    for posicion, caracter in enumerate(isbn[:12]):

        digito = int(caracter)

        if posicion % 2 == 0:
            suma += digito
        else:
            suma += digito * 3

    digito_control = (10 - (suma % 10)) % 10

    return digito_control == int(isbn[12])


def es_issn_valido(valor):
    """
    Verifica si un valor es un ISSN válido.
    """

    issn = normalizar_identificador(valor)

    if len(issn) != 8:
        return False

    if not re.fullmatch(r"[0-9]{7}[0-9X]", issn):
        return False

    suma = 0

    for posicion, caracter in enumerate(issn, start=0):

        if caracter == "X":
            digito = 10
        else:
            digito = int(caracter)

        suma += digito * (8 - posicion)

    return suma % 11 == 0


def clasificar_identificador(valor):
    """
    Clasifica un identificador bibliográfico.
    """

    if valor is None or str(valor).strip() == "":
        return "VACIO"

    normalizado = normalizar_identificador(valor)

    if len(normalizado) == 10:

        if es_isbn_10_valido(normalizado):
            return "ISBN-10"

        return "ISBN-10 INVÁLIDO"

    if len(normalizado) == 13:

        if es_isbn_13_valido(normalizado):
            return "ISBN-13"

        return "ISBN-13 INVÁLIDO"

    if len(normalizado) == 8:

        if es_issn_valido(normalizado):
            return "ISSN"

        return "ISSN INVÁLIDO"

    return "NO IDENTIFICADO"