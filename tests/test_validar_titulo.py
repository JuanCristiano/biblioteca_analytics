import json

from modulos.calidad_datos.auditor import auditar_catalogo


ruta = "data/raw/catalogo_marc_prueba.json"

with open(ruta, "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)


errores = auditar_catalogo(catalogo)

for error in errores:
    print(error)