import json

from modulos.calidad_datos.reglas.detectar_duplicados import detectar_isbn_duplicados


ruta = "data/raw/catalogo_marc_prueba.json"

with open(ruta, "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)


errores = detectar_isbn_duplicados(catalogo)

for error in errores:
    print(error)