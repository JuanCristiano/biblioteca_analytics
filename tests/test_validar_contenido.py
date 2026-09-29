import pytest

from modulos.cargadores.validar_contenido import (
    clasificar_identificador,
    es_isbn10,
    es_isbn13,
    es_issn,
    normalizar_identificador,
)


# ---------- normalizar_identificador ----------

@pytest.mark.parametrize("valor, esperado", [
    ("978-0-306-40615-7", "9780306406157"),
    (" 0 306 ", "0306"),
    ("080442957x", "080442957X"),
    (9780306406157, "9780306406157"),
    (None, ""),
    ("", ""),
])
def test_normalizar_identificador(valor, esperado):
    assert normalizar_identificador(valor) == esperado


# ---------- es_isbn13 ----------

@pytest.mark.parametrize("valor", [
    "9780306406157",
    "978-0-306-40615-7",
    "978 0 306 40615 7",
    "9780140328721",
    "9789501234565",
])
def test_isbn13_valido(valor):
    assert es_isbn13(valor) is True


@pytest.mark.parametrize("valor", [
    "9789501234567",        # dígito de control incorrecto (debería ser 5)
    "978030640615",         # 12 dígitos
    "97803064061577",       # 14 dígitos
    "978030640615X",        # la X solo existe en ISBN-10 e ISSN
    "abcdefghijklm",
    "",
    None,
])
def test_isbn13_invalido(valor):
    assert es_isbn13(valor) is False


def test_isbn13_acepta_un_numero_entero():
    assert es_isbn13(9780306406157) is True


# ---------- es_isbn10 ----------

@pytest.mark.parametrize("valor", [
    "0-306-40615-2",
    "0306406152",
    "9501234568",
    "080442957X",
    "080442957x",
    "0 8044 2957 X",
])
def test_isbn10_valido(valor):
    assert es_isbn10(valor) is True


@pytest.mark.parametrize("valor", [
    "9501234567",           # dígito de control incorrecto (debería ser 8)
    "0306406153",           # cambia solo el último dígito
    "030640615",            # 9 dígitos
    "03064061522",          # 11 dígitos
    "0306406A52",           # letra en el medio
    "X306406152",           # la X solo puede ir al final
    "",
    None,
])
def test_isbn10_invalido(valor):
    assert es_isbn10(valor) is False


# ---------- es_issn ----------

@pytest.mark.parametrize("valor", [
    "2049-3630",
    "20493630",
    "0317-8471",
    "2434-561X",
    "2434-561x",
])
def test_issn_valido(valor):
    assert es_issn(valor) is True


@pytest.mark.parametrize("valor", [
    "12345678",             # 8 dígitos, pero el dígito de control no cierra
    "2049-3631",            # cambia solo el último dígito
    "2049363",              # 7 dígitos
    "204936300",            # 9 dígitos
    "X2493630",             # la X solo puede ir al final
    "",
    None,
])
def test_issn_invalido(valor):
    assert es_issn(valor) is False


# ---------- Un identificador válido no se confunde con otro tipo ----------

def test_cada_funcion_solo_acepta_su_propio_tipo():
    assert (es_isbn10("0306406152"), es_isbn13("0306406152"), es_issn("0306406152")) == (True, False, False)
    assert (es_isbn10("9780306406157"), es_isbn13("9780306406157"), es_issn("9780306406157")) == (False, True, False)
    assert (es_isbn10("2049-3630"), es_isbn13("2049-3630"), es_issn("2049-3630")) == (False, False, True)


# ---------- clasificar_identificador ----------

@pytest.mark.parametrize("valor, esperado", [
    ("9780306406157", "ISBN-13"),
    ("978-0-306-40615-7", "ISBN-13"),
    ("9789501234565", "ISBN-13"),
    ("9789501234567", "ISBN-13 INVÁLIDO"),
    ("978-950-12-3456-7", "ISBN-13 INVÁLIDO"),
    ("0-306-40615-2", "ISBN-10"),
    ("0306406152", "ISBN-10"),
    ("080442957X", "ISBN-10"),
    ("9501234567", "ISBN-10 INVÁLIDO"),
    ("2049-3630", "ISSN"),
    ("20493630", "ISSN"),
    ("0317-8471", "ISSN"),
    ("2434-561X", "ISSN"),
    ("12345678", "ISSN INVÁLIDO"),
    ("97895012345", "NO IDENTIFICADO"),
    ("Juan Pérez", "NO IDENTIFICADO"),
    ("", "VACIO"),
    ("   ", "VACIO"),
    (None, "VACIO"),
])
def test_clasificar_identificador(valor, esperado):
    assert clasificar_identificador(valor) == esperado


def test_clasificar_acepta_un_numero_entero():
    assert clasificar_identificador(9780306406157) == "ISBN-13"


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

def test_limitacion_el_prefijo_isbn_no_se_elimina():
    assert clasificar_identificador("ISBN 0-306-40615-2") == "NO IDENTIFICADO"


def test_limitacion_un_isbn10_leido_como_numero_pierde_el_cero_inicial():
    # Pasa cuando una planilla convierte 0306406152 en el número 306406152.
    assert es_isbn10(306406152) is False
    assert clasificar_identificador(306406152) == "NO IDENTIFICADO"


def test_limitacion_una_x_en_un_isbn13_no_se_reconoce_como_invalido():
    assert clasificar_identificador("978030640615X") == "NO IDENTIFICADO"