from modulos.cargadores.cargar_csv import cargar_catalogo_csv


RUTA_CSV = (
    "data/raw/catalogo_prueba.csv"
)


catalogo = cargar_catalogo_csv(
    RUTA_CSV
)


print(
    f"Cantidad de registros: {len(catalogo)}"
)

print()

for registro in catalogo:
    print(
        registro["001"],
        "-",
        registro["titulo"]
    )