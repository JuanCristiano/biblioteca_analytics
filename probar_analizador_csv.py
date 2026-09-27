from modulos.cargadores.analizar_csv import analizar_csv


RUTA_CSV = (
    "data/raw/catalogo_prueba.csv"
)


resultado = analizar_csv(
    RUTA_CSV
)


print("ANÁLISIS DEL ARCHIVO")
print("====================")
print()

print(
    f"Separador detectado: "
    f"{repr(resultado['separador'])}"
)

print()

print("Columnas detectadas:")

for columna in resultado["columnas"]:
    print(
        f"- {columna}"
    )