from modulos.cargadores.validar_contenido import (
    es_isbn10,
    es_isbn13,
    es_issn,
    clasificar_identificador
)


valores_prueba = [

    # ISBN-13
    "9789501234567",
    "978-950-12-3456-7",

    # ISBN-10
    "9501234567",
    "0-306-40615-2",

    # ISSN
    "2049-3630",
    "20493630",

    # ISSN con X
    "0317-8471",

    # Valores incorrectos
    "97895012345",
    "12345678",
    "Juan Pérez",
    "",
    None
]


print("VALIDACIÓN DE IDENTIFICADORES")
print("=============================")

for valor in valores_prueba:

    print()
    print(f"Valor: {valor}")
    print(f"ISBN-10: {es_isbn10(valor)}")
    print(f"ISBN-13: {es_isbn13(valor)}")
    print(f"ISSN: {es_issn(valor)}")
    print(f"Clasificación: {clasificar_identificador(valor)}")