import json

from modulos.calidad_datos.auditor import auditar_catalogo
from modulos.calidad_datos.resumen import resumir_resultados
from modulos.calidad_datos.exportar_resumen_csv import exportar_resumen_csv


ruta = "data/raw/catalogo_marc_prueba.json"

with open(ruta, "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)


errores = auditar_catalogo(catalogo)

resumen = resumir_resultados(
    catalogo,
    errores
)

ruta_salida = "data/processed/resumen_calidad.csv"

exportar_resumen_csv(
    resumen["indicadores_por_regla"],
    ruta_salida
)

print(f"CSV generado: {ruta_salida}")