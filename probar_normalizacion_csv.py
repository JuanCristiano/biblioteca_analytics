from modulos.cargadores.normalizar_csv import (
    normalizar_catalogo_csv
)


RUTA_CSV = (
    "data/raw/catalogo_prueba_3.csv"
)


resultado = normalizar_catalogo_csv(
    RUTA_CSV
)


print("NORMALIZACIÓN DEL CATÁLOGO")
print("==========================")
print()

print("Columnas originales:")

for columna in resultado["columnas_originales"]:
    print(
        f"- {columna}"
    )

print()

print("Mapeo detectado:")

for original, estandar in resultado["mapeo"].items():
    print(
        f"- {original} → {estandar}"
    )

print()

print("Columnas desconocidas:")

for columna in resultado["columnas_desconocidas"]:
    print(
        f"- {columna}"
    )

print(
    f"Registros normalizados: "
    f"{len(resultado['catalogo'])}"
)

print()

print("Primer registro:")

print(
    resultado["catalogo"][0]
)