"""
Adaptador entre el catálogo "plano" que produce normalizar_catalogo_csv
(un dict por registro con claves como "titulo", "autor", "isbn", etc.)
y la estructura MARC anidada que ya consumen las reglas de calidad
(registro["245"][0]["subcampos"]["a"], etc.).

Esto permite que las reglas de modulos/calidad_datos/reglas/ no tengan
que saber nunca de dónde vino el registro (JSON ya en MARC, o CSV con
columnas variables): siempre reciben la misma forma.
"""


def convertir_registro_a_marc(registro_plano):

    marc = {}

    marc["001"] = registro_plano.get("001", "").strip()

    isbn = registro_plano.get("isbn", "").strip()

    if isbn:
        marc["020"] = [
            {"subcampos": {"a": isbn}}
        ]

    autor = registro_plano.get("autor", "").strip()

    if autor:
        marc["100"] = [
            {"subcampos": {"a": autor}}
        ]

    titulo = registro_plano.get("titulo", "").strip()

    if titulo:
        marc["245"] = [
            {"subcampos": {"a": titulo}}
        ]

    editorial = registro_plano.get("editorial", "").strip()
    anio = registro_plano.get("anio", "").strip()

    if editorial or anio:

        subcampos_264 = {}

        if editorial:
            subcampos_264["b"] = editorial

        if anio:
            subcampos_264["c"] = anio

        marc["264"] = [
            {"subcampos": subcampos_264}
        ]

    # Nota: el campo 300 (descripción física: páginas, tamaño) no tiene
    # equivalente en un CSV típico de catálogo. Se deja sin completar
    # a propósito: la REGLA-006 va a advertir su ausencia, que es el
    # comportamiento correcto (si no vino el dato, corresponde avisar).

    # Campos sin regla de calidad todavía, pero que no queremos perder:
    ubicacion = registro_plano.get("ubicacion", "").strip()

    if ubicacion:
        marc["852"] = [
            {"subcampos": {"a": ubicacion}}
        ]

    codigo_barras = registro_plano.get("codigo_barras", "").strip()

    if codigo_barras:
        marc["952"] = [
            {"subcampos": {"p": codigo_barras}}
        ]

    tipo_material = registro_plano.get("tipo_material", "").strip()

    if tipo_material:
        # Metadato de control, no es un campo MARC de contenido.
        marc["_tipo_material"] = tipo_material

    return marc


def convertir_catalogo_a_marc(catalogo_plano):

    return [
        convertir_registro_a_marc(registro)
        for registro in catalogo_plano
    ]
