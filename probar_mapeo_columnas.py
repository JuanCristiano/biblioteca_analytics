from modulos.cargadores.mapear_columnas import (
    mapear_columna
)


columnas_prueba = [
    "001",
    "Título",
    "Autor principal",
    "ISBN-13",
    "Publisher",
    "Año publicación",
    "Campo desconocido"
]


print("MAPEO DE COLUMNAS")
print("=================")
print()

for columna in columnas_prueba:

    resultado = mapear_columna(
        columna
    )

    print(
        f"{columna} → {resultado}"
    )