import json

ruta = "data/raw/catalogo_marc_prueba.json"

with open(ruta, "r", encoding="utf-8") as archivo:
    catalogo = json.load(archivo)

print(f"Cantidad de registros: {len(catalogo)}")

for registro in catalogo:
    print(
        registro["001"],
        "-",
        registro.get("245", [{}])[0].get("subcampos", {}).get("a", "[SIN TÍTULO]")
    )