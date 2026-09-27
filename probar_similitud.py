from similitud_texto import calcular_similitud


pruebas = [
    ("Fantastic Mr. Fox", "Fantastic Mr Fox"),
    ("Fantastic Mr. Fox", "Fantastic Mr. Foz"),
    ("Fantastic Mr. Fox", "Fantastic Mr. Foxx"),
    ("Fantastic Mr. Fox", "Charlie y la fábrica de chocolate"),
    ("Roald Dahl", "Roald Dhal"),
    ("Roald Dahl", "J. K. Rowling"),

    ("Gabriel García Márquez", "Gabriel Garcia Marquez"),
    ("Gabriel García Márquez", "Gabriel Garcia Marque"),
    ("Gabriel García Márquez", "Gabriel García Marquez"),
    ("Gabriel García Márquez", "Gabrial García Márquez"),
    ("Gabriel García Márquez", "García Márquez, Gabriel")
]


print("PRUEBAS DE SIMILITUD")
print("====================")
print()


for texto1, texto2 in pruebas:

    similitud = calcular_similitud(texto1, texto2)

    print(f"Texto 1: {texto1}")
    print(f"Texto 2: {texto2}")
    print(f"Similitud: {similitud:.4f}")
    print("-" * 50)