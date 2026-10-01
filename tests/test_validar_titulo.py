import json
from pathlib import Path

from modulos.calidad_datos.auditor import auditar_catalogo

RUTA = Path(__file__).resolve().parent.parent / "data" / "raw" / "catalogo_marc_prueba.json"


def cargar_catalogo():
    with open(RUTA, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def test_detecta_titulo_vacio_en_registro_000008():
    errores = auditar_catalogo(cargar_catalogo())

    titulo_vacio = [
        e for e in errores
        if e["registro"] == "000008" and e["regla"] == "REGLA-001"
    ]

    assert len(titulo_vacio) == 1
    assert titulo_vacio[0]["nivel"] == "ERROR"
    assert titulo_vacio[0]["campo"] == "245"