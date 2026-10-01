import json
from pathlib import Path

from modulos.calidad_datos.reglas.detectar_duplicados import detectar_isbn_duplicados

RUTA = Path(__file__).resolve().parent.parent / "data" / "raw" / "catalogo_marc_prueba.json"


def cargar_catalogo():
    with open(RUTA, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def test_detecta_isbn_duplicado_entre_000009_y_000001():
    errores = detectar_isbn_duplicados(cargar_catalogo())

    assert len(errores) == 1

    error = errores[0]
    assert error["registro"] == "000009"
    assert error["regla"] == "REGLA-003"
    assert error["nivel"] == "ADVERTENCIA"
    assert "000001" in error["problema"]