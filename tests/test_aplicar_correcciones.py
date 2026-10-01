import copy
from pathlib import Path

import pytest

from modulos.calidad_datos.aplicar_correcciones import aplicar_correcciones
from modulos.calidad_datos.auditor import auditar_catalogo
from modulos.cargadores.cargar_fuente_autores import cargar_fuente_autores
from modulos.cargadores.cargar_json import cargar_catalogo_json

RAIZ = Path(__file__).resolve().parent.parent
RUTA_CATALOGO_200 = RAIZ / "data" / "raw" / "catalogo_marc_prueba_200.json"
RUTA_FUENTE_AUTORES_200 = RAIZ / "data" / "raw" / "fuente_autores_prueba_200.csv"

CORRECCIONES_200 = [
    {"001": "000036", "campo": "264", "subcampo": "c",
     "valor_nuevo": "2020", "motivo": "Completar año de publicación"},
    {"001": "000039", "campo": "245", "subcampo": "b",
     "valor_nuevo": "Una introducción", "motivo": "Completar subtítulo"},
    {"001": "000048", "campo": "300", "subcampo": "a",
     "valor_nuevo": "245 páginas", "motivo": "Completar extensión física"},
]


# ---------- Datos y ayudantes ----------

def catalogo_ejemplo():
    return [
        {
            "001": "000001",
            "245": [{"indicadores": ["1", "0"],
                     "subcampos": {"a": "Rayuela", "c": "Julio Cortázar"}}],
            "650": [
                {"subcampos": {"a": "Novela"}},
                {"subcampos": {"a": "Literatura argentina", "x": "Historia"}},
            ],
        },
        {"001": "000002", "245": [{"subcampos": {"a": ""}}]},
        {"001": "000003"},
    ]


def correccion(**cambios):
    datos = {
        "001": "000001",
        "campo": "245",
        "subcampo": "a",
        "valor_nuevo": "Rayuela (2.ª ed.)",
        "motivo": "Corrección manual",
    }
    datos.update(cambios)
    return datos


def aplicar_datos(datos, catalogo=None):
    catalogo = catalogo if catalogo is not None else catalogo_ejemplo()
    corregido, historial = aplicar_correcciones(catalogo, [datos])
    return corregido, historial[0]


def aplicar_una(catalogo, **cambios):
    return aplicar_datos(correccion(**cambios), catalogo)


def registro(catalogo, identificador):
    return next(r for r in catalogo if r.get("001") == identificador)


def subcampos_245(catalogo, identificador="000001"):
    return registro(catalogo, identificador)["245"][0]["subcampos"]


# ---------- Correcciones que se aplican ----------

def test_reemplaza_un_subcampo_existente_y_lo_registra_en_el_historial():
    corregido, historial = aplicar_correcciones(catalogo_ejemplo(), [correccion()])

    assert subcampos_245(corregido)["a"] == "Rayuela (2.ª ed.)"
    assert historial == [{
        "001": "000001",
        "campo": "245",
        "subcampo": "a",
        "valor_anterior": "Rayuela",
        "valor_nuevo": "Rayuela (2.ª ed.)",
        "resultado": "APLICADA",
        "motivo": "Corrección manual",
    }]


def test_completa_un_subcampo_vacio():
    corregido, item = aplicar_una(
        catalogo_ejemplo(), **{"001": "000002"}, valor_nuevo="Título completo"
    )

    assert subcampos_245(corregido, "000002")["a"] == "Título completo"
    assert item["valor_anterior"] == ""
    assert item["resultado"] == "APLICADA"


def test_agrega_un_subcampo_que_no_existe_en_un_campo_existente():
    corregido, item = aplicar_una(catalogo_ejemplo(), subcampo="b", valor_nuevo="Un juego")

    assert subcampos_245(corregido) == {"a": "Rayuela", "c": "Julio Cortázar", "b": "Un juego"}
    assert item["valor_anterior"] == ""
    assert item["resultado"] == "APLICADA"


def test_crea_el_campo_si_el_registro_no_lo_tiene():
    corregido, item = aplicar_una(
        catalogo_ejemplo(),
        **{"001": "000003", "campo": "300", "subcampo": "a", "valor_nuevo": "245 páginas"},
    )

    assert registro(corregido, "000003") == {
        "001": "000003",
        "300": [{"subcampos": {"a": "245 páginas"}}],
    }
    assert item["valor_anterior"] == ""
    assert item["resultado"] == "APLICADA"


def test_conserva_el_resto_de_los_datos():
    original = catalogo_ejemplo()

    corregido, _ = aplicar_una(catalogo_ejemplo())

    modificado = registro(corregido, "000001")
    assert modificado["245"][0]["indicadores"] == ["1", "0"]
    assert modificado["245"][0]["subcampos"]["c"] == "Julio Cortázar"
    assert modificado["650"] == registro(original, "000001")["650"]
    assert registro(corregido, "000002") == registro(original, "000002")
    assert registro(corregido, "000003") == registro(original, "000003")


# ---------- Campos repetibles (650 tiene dos elementos) ----------

def test_en_un_campo_repetible_corrige_el_primer_elemento_que_tiene_el_subcampo():
    corregido, item = aplicar_una(catalogo_ejemplo(), campo="650", valor_nuevo="Cuento")

    elementos = registro(corregido, "000001")["650"]
    assert elementos[0]["subcampos"]["a"] == "Cuento"
    assert elementos[1]["subcampos"]["a"] == "Literatura argentina"
    assert item["valor_anterior"] == "Novela"


def test_en_un_campo_repetible_corrige_el_segundo_si_solo_el_tiene_el_subcampo():
    corregido, item = aplicar_una(
        catalogo_ejemplo(), campo="650", subcampo="x", valor_nuevo="Crítica"
    )

    elementos = registro(corregido, "000001")["650"]
    assert elementos[0]["subcampos"] == {"a": "Novela"}
    assert elementos[1]["subcampos"] == {"a": "Literatura argentina", "x": "Crítica"}
    assert item["valor_anterior"] == "Historia"


def test_en_un_campo_repetible_agrega_el_subcampo_al_primer_elemento_si_ninguno_lo_tiene():
    corregido, item = aplicar_una(
        catalogo_ejemplo(), campo="650", subcampo="z", valor_nuevo="Argentina"
    )

    elementos = registro(corregido, "000001")["650"]
    assert elementos[0]["subcampos"] == {"a": "Novela", "z": "Argentina"}
    assert elementos[1]["subcampos"] == {"a": "Literatura argentina", "x": "Historia"}
    assert item["valor_anterior"] == ""


# ---------- El catálogo original no se toca ----------

def test_no_modifica_el_catalogo_original():
    original = catalogo_ejemplo()
    copia = copy.deepcopy(original)
    correcciones = [
        correccion(),
        correccion(**{"001": "000003", "campo": "300", "subcampo": "a", "valor_nuevo": "x"}),
    ]

    corregido, _ = aplicar_correcciones(original, correcciones)

    assert original == copia
    assert corregido != original


def test_sin_correcciones_devuelve_una_copia_igual():
    original = catalogo_ejemplo()

    corregido, historial = aplicar_correcciones(original, [])

    assert historial == []
    assert corregido == original
    assert corregido is not original
    assert corregido[0] is not original[0]


def test_con_un_catalogo_vacio_ninguna_correccion_se_aplica():
    corregido, historial = aplicar_correcciones(
        [], [correccion(), correccion(**{"001": "000002"})]
    )

    assert corregido == []
    assert [h["resultado"] for h in historial] == ["NO APLICADA", "NO APLICADA"]
    assert {h["motivo"] for h in historial} == {"Registro no encontrado"}


# ---------- Correcciones que no se aplican ----------

def test_registro_no_encontrado():
    corregido, item = aplicar_una(catalogo_ejemplo(), **{"001": "999999"})

    # Ojo: en el historial el "motivo" pasa a ser la razón del fallo,
    # y el motivo que traía la corrección ("Corrección manual") se pierde.
    assert item == {
        "001": "999999",
        "campo": "245",
        "subcampo": "a",
        "resultado": "NO APLICADA",
        "motivo": "Registro no encontrado",
    }
    assert corregido == catalogo_ejemplo()


@pytest.mark.parametrize("campo", ["", "   "])
def test_campo_vacio_no_se_aplica(campo):
    corregido, item = aplicar_una(catalogo_ejemplo(), campo=campo)

    assert item == {
        "001": "000001",
        "campo": "",
        "subcampo": "a",
        "resultado": "NO APLICADA",
        "motivo": "Campo MARC no informado",
    }
    assert corregido == catalogo_ejemplo()


def test_campo_ausente_no_se_aplica():
    datos = correccion()
    del datos["campo"]

    corregido, item = aplicar_datos(datos)

    assert item["resultado"] == "NO APLICADA"
    assert item["motivo"] == "Campo MARC no informado"
    assert corregido == catalogo_ejemplo()


@pytest.mark.parametrize("subcampo", ["", "   "])
def test_subcampo_vacio_no_se_aplica(subcampo):
    corregido, item = aplicar_una(catalogo_ejemplo(), subcampo=subcampo)

    assert item == {
        "001": "000001",
        "campo": "245",
        "subcampo": "",
        "resultado": "NO APLICADA",
        "motivo": "Subcampo no informado",
    }
    assert corregido == catalogo_ejemplo()


def test_subcampo_ausente_no_se_aplica():
    datos = correccion()
    del datos["subcampo"]

    corregido, item = aplicar_datos(datos)

    assert item["resultado"] == "NO APLICADA"
    assert item["motivo"] == "Subcampo no informado"
    assert corregido == catalogo_ejemplo()


def test_si_el_registro_no_existe_eso_se_informa_antes_que_un_campo_vacio():
    _, item = aplicar_una(catalogo_ejemplo(), **{"001": "999999"}, campo="")

    assert item["motivo"] == "Registro no encontrado"


def test_si_faltan_campo_y_subcampo_se_informa_el_campo():
    _, item = aplicar_una(catalogo_ejemplo(), campo="", subcampo="")

    assert item["motivo"] == "Campo MARC no informado"


# ---------- Varias correcciones juntas ----------

def test_el_historial_sigue_el_orden_de_las_correcciones():
    correcciones = [
        correccion(),
        correccion(**{"001": "999999"}),
        correccion(**{"001": "000002"}, valor_nuevo="Título completo"),
        correccion(campo=""),
    ]

    corregido, historial = aplicar_correcciones(catalogo_ejemplo(), correcciones)

    assert [(h["001"], h["resultado"]) for h in historial] == [
        ("000001", "APLICADA"),
        ("999999", "NO APLICADA"),
        ("000002", "APLICADA"),
        ("000001", "NO APLICADA"),
    ]
    assert subcampos_245(corregido)["a"] == "Rayuela (2.ª ed.)"
    assert subcampos_245(corregido, "000002")["a"] == "Título completo"


def test_dos_correcciones_sobre_el_mismo_subcampo_se_encadenan():
    corregido, historial = aplicar_correcciones(
        catalogo_ejemplo(),
        [correccion(valor_nuevo="Primera"), correccion(valor_nuevo="Segunda")],
    )

    assert [h["valor_anterior"] for h in historial] == ["Rayuela", "Primera"]
    assert [h["valor_nuevo"] for h in historial] == ["Primera", "Segunda"]
    assert subcampos_245(corregido)["a"] == "Segunda"


def test_ignora_los_espacios_alrededor_de_id_campo_y_subcampo():
    corregido, item = aplicar_una(
        catalogo_ejemplo(), **{"001": " 000001 "}, campo=" 245 ", subcampo=" a "
    )

    assert (item["001"], item["campo"], item["subcampo"]) == ("000001", "245", "a")
    assert item["resultado"] == "APLICADA"
    assert subcampos_245(corregido)["a"] == "Rayuela (2.ª ed.)"


def test_el_motivo_se_limpia_y_es_opcional():
    _, con_espacios = aplicar_una(catalogo_ejemplo(), motivo="  Corrección  ")
    datos = correccion()
    del datos["motivo"]
    _, sin_motivo = aplicar_datos(datos)

    assert con_espacios["motivo"] == "Corrección"
    assert sin_motivo["motivo"] == ""


# ---------- Catálogo de prueba de 200 registros ----------
# Depende de data/raw/catalogo_marc_prueba_200.json y fuente_autores_prueba_200.csv:
# es material de prueba fijo. Si lo cambiás a propósito, actualizá estos valores.

@pytest.fixture
def catalogo_200():
    return cargar_catalogo_json(RUTA_CATALOGO_200)


@pytest.fixture
def fuente_autores_200():
    return cargar_fuente_autores(RUTA_FUENTE_AUTORES_200)


def test_las_tres_correcciones_reducen_las_alertas_de_21_a_18(catalogo_200, fuente_autores_200):
    antes = auditar_catalogo(catalogo_200, fuente_autores_200)

    corregido, historial = aplicar_correcciones(catalogo_200, CORRECCIONES_200)
    despues = auditar_catalogo(corregido, fuente_autores_200)

    assert len(catalogo_200) == 200
    assert len(antes) == 21
    assert [h["resultado"] for h in historial] == ["APLICADA"] * 3
    assert len(despues) == 18
    assert round((len(antes) - len(despues)) / len(antes) * 100, 1) == 14.3
    # El catálogo original sigue teniendo las 21 alertas.
    assert len(auditar_catalogo(catalogo_200, fuente_autores_200)) == 21


def test_historial_de_correcciones_del_catalogo_de_200(catalogo_200):
    corregido, historial = aplicar_correcciones(catalogo_200, CORRECCIONES_200)

    assert [
        (h["001"], h["campo"], h["subcampo"], h["valor_anterior"], h["valor_nuevo"])
        for h in historial
    ] == [
        ("000036", "264", "c", "", "2020"),
        ("000039", "245", "b", "", "Una introducción"),
        ("000048", "300", "a", "", "245 páginas"),
    ]
    for identificador, campo, subcampo, valor in [
        ("000036", "264", "c", "2020"),
        ("000039", "245", "b", "Una introducción"),
        ("000048", "300", "a", "245 páginas"),
    ]:
        elementos = registro(corregido, identificador)[campo]
        assert any(e.get("subcampos", {}).get(subcampo) == valor for e in elementos)


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

def test_limitacion_una_correccion_sin_valor_nuevo_borra_el_subcampo():
    datos = correccion()
    del datos["valor_nuevo"]

    corregido, item = aplicar_datos(datos)

    assert item["resultado"] == "APLICADA"
    assert item["valor_nuevo"] == ""
    assert subcampos_245(corregido)["a"] == ""


def test_limitacion_el_valor_nuevo_se_guarda_tal_cual():
    corregido_numero, _ = aplicar_una(catalogo_ejemplo(), valor_nuevo=2020)
    corregido_espacios, _ = aplicar_una(catalogo_ejemplo(), valor_nuevo=" Rayuela ")

    assert subcampos_245(corregido_numero)["a"] == 2020
    assert isinstance(subcampos_245(corregido_numero)["a"], int)
    assert subcampos_245(corregido_espacios)["a"] == " Rayuela "


def test_limitacion_un_id_numerico_pierde_los_ceros_iniciales():
    # Pasa cuando las correcciones vienen de una planilla que convirtió 000001 en 1.
    corregido, item = aplicar_una(catalogo_ejemplo(), **{"001": 1})

    assert item["001"] == "1"
    assert item["resultado"] == "NO APLICADA"
    assert corregido == catalogo_ejemplo()


def test_limitacion_un_campo_none_se_toma_como_el_texto_none():
    corregido, item = aplicar_una(catalogo_ejemplo(), campo=None)

    assert item["resultado"] == "APLICADA"
    assert item["campo"] == "None"
    assert "None" in registro(corregido, "000001")


def test_limitacion_con_001_duplicados_solo_se_corrige_el_ultimo():
    catalogo = [
        {"001": "000001", "245": [{"subcampos": {"a": "Primero"}}]},
        {"001": "000001", "245": [{"subcampos": {"a": "Segundo"}}]},
    ]

    corregido, item = aplicar_una(catalogo)

    assert item["valor_anterior"] == "Segundo"
    assert corregido[0]["245"][0]["subcampos"]["a"] == "Primero"
    assert corregido[1]["245"][0]["subcampos"]["a"] == "Rayuela (2.ª ed.)"