from comparar_autores import comparar_multiples_autores


# ====================================================
# PRUEBAS DE MÚLTIPLES AUTORES
# ====================================================

casos = [

    # ------------------------------------------------
    # 1. Coincidencia exacta
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 2. Orden diferente
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Adolfo Bioy Casares; Jorge Luis Borges"
    ),

    # ------------------------------------------------
    # 3. Apellido, Nombre
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Borges, Jorge Luis; Bioy Casares, Adolfo"
    ),

    # ------------------------------------------------
    # 4. Error de escritura
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borge; Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 5. Autor faltante
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges"
    ),

    # ------------------------------------------------
    # 6. Autor adicional
    # ------------------------------------------------

    (
        "Jorge Luis Borges",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 7. Autor reemplazado
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges; Julio Cortázar"
    ),

    # ------------------------------------------------
    # 8. Separador /
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges / Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 9. Separador y
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges y Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 10. Separadores mezclados
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares; Julio Cortázar",
        "Julio Cortázar / Jorge Luis Borges y Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 11. Diferencia de mayúsculas
    # ------------------------------------------------

    (
        "JORGE LUIS BORGES; ADOLFO BIOY CASARES",
        "jorge luis borges; adolfo bioy casares"
    ),

    # ------------------------------------------------
    # 12. Espacios diferentes
    # ------------------------------------------------

    (
        "Jorge   Luis   Borges; Adolfo   Bioy   Casares",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 13. Dos errores
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borge; Adolfo Bioy Cazares"
    ),

    # ------------------------------------------------
    # 14. Iniciales
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "J. L. Borges; A. Bioy Casares"
    ),

    # ------------------------------------------------
    # 15. Nombre con rol
    # ------------------------------------------------

    (
        "Jorge Luis Borges",
        "Jorge Luis Borges (autor)"
    ),

    # ------------------------------------------------
    # 16. Autor duplicado
    # ------------------------------------------------

    (
        "Jorge Luis Borges",
        "Jorge Luis Borges; Jorge Luis Borges"
    ),

    # ------------------------------------------------
    # 17. Caso ambiguo con comas
    # ------------------------------------------------

    (
        "Jorge Luis Borges, Adolfo Bioy Casares",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),

    # ------------------------------------------------
    # 18. Autoridad institucional
    # ------------------------------------------------

    (
        "UNESCO",
        "United Nations Educational, Scientific and Cultural Organization"
    ),

    # ------------------------------------------------
    # 19. Campo vacío
    # ------------------------------------------------

    (
        "",
        "Jorge Luis Borges"
    ),

    # ------------------------------------------------
    # 20. None
    # ------------------------------------------------

    (
        None,
        "Jorge Luis Borges"
    ),
]


# ====================================================
# EJECUCIÓN
# ====================================================

print("=" * 60)
print("PRUEBA DE COMPARACIÓN DE MÚLTIPLES AUTORES")
print("=" * 60)


for numero, (catalogo, fuente) in enumerate(casos, start=1):

    resultado = comparar_multiples_autores(
        catalogo,
        fuente
    )

    print()
    print("-" * 60)
    print(f"PRUEBA {numero}")
    print("-" * 60)

    print(f"Catálogo : {catalogo}")
    print(f"Fuente   : {fuente}")

    print()
    print(f"Resultado : {resultado['resultado']}")
    print(f"Motivo   : {resultado['motivo']}")

    print(
        f"Cantidad catálogo: "
        f"{resultado['cantidad_catalogo']}"
    )

    print(
        f"Cantidad fuente  : "
        f"{resultado['cantidad_fuente']}"
    )

    if resultado["coincidencias"]:

        print()
        print("Coincidencias:")

        for coincidencia in resultado["coincidencias"]:

            print(
                f"  - {coincidencia['catalogo']} "
                f"↔ {coincidencia['fuente']}"
            )

    if resultado["posibles_coincidencias"]:

        print()
        print("Posibles coincidencias:")

        for posible in resultado["posibles_coincidencias"]:

            print(
                f"  - {posible['catalogo']} "
                f"↔ {posible['fuente']} "
                f"(similitud: {posible['similitud']})"
            )

    if resultado["faltantes"]:

        print()
        print("Autores faltantes:")

        for autor in resultado["faltantes"]:

            print(f"  - {autor}")

    if resultado["adicionales"]:

        print()
        print("Autores adicionales:")

        for autor in resultado["adicionales"]:

            print(f"  - {autor}")


print()
print("=" * 60)
print("FIN DE LAS PRUEBAS")
print("=" * 60)