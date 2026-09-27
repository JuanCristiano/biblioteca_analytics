import json

from modulos.calidad_datos.auditor import auditar_catalogo
from modulos.calidad_datos.resumen import resumir_resultados
from modulos.calidad_datos.informe import generar_informe


ruta = "data/raw/catalogo_marc_prueba.json"

with open(ruta, "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)


errores = auditar_catalogo(catalogo)

resumen = resumir_resultados(catalogo, errores)

informe = generar_informe(resumen, errores)

print(informe)