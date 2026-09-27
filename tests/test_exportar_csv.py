import json

from modulos.calidad_datos.auditor import auditar_catalogo
from modulos.calidad_datos.exportar_csv import exportar_errores_csv


ruta = "data/raw/catalogo_marc_prueba.json"

with open(ruta, "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)


errores = auditar_catalogo(catalogo)

ruta_salida = "data/processed/auditoria_catalogo.csv"

exportar_errores_csv(
    errores,
    ruta_salida
)

print(f"CSV generado: {ruta_salida}")