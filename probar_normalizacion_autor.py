from normalizacion import normalizar_autor


pruebas = [
    "Gabriel García Márquez",
    "Gabriel Garcia Marquez",
    "García Márquez, Gabriel",
    "Garcia Marquez, Gabriel",
    "García Márquez Gabriel",
    "Gabrial García Márquez",
]


print("NORMALIZACIÓN DE AUTORES")
print("========================")
print()

for autor in pruebas:

    resultado = normalizar_autor(autor)

    print(f"Original:    {autor}")
    print(f"Normalizado: {resultado}")
    print("-" * 50)