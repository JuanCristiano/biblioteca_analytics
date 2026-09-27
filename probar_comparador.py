from fuentes_bibliograficas import consultar_openlibrary
from comparador_bibliografico import comparar_registro


# ----------------------------------------------------
# REGISTRO DE NUESTRO CATÁLOGO
# ----------------------------------------------------

registro_catalogo = {
    "isbn": "9780140328721",
    "titulo": "  Fantastic    Mr. Foz  ",
    "autor": "ROALD DAHL",
    "editorial": "puffin"
}


# ----------------------------------------------------
# CONSULTA EXTERNA
# ----------------------------------------------------

registro_externo = consultar_openlibrary(
    registro_catalogo["isbn"]
)


# ----------------------------------------------------
# COMPARACIÓN
# ----------------------------------------------------

resultado = comparar_registro(
    registro_catalogo,
    registro_externo
)


print("COMPARACIÓN BIBLIOGRÁFICA")
print("=========================")

print()

print("REGISTRO DEL CATÁLOGO")
print("---------------------")

for clave, valor in registro_catalogo.items():
    print(f"{clave}: {valor}")

print()

print("FUENTE EXTERNA")
print("--------------")

for clave, valor in registro_externo.items():
    print(f"{clave}: {valor}")

print()

print("RESULTADO")
print("--------")

for clave, valor in resultado.items():
    print(f"{clave}: {valor}")