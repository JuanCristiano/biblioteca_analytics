from comparar_autores import comparar_autor


# ====================================================
# BATERÍA DE PRUEBAS DE AUTORES
# ====================================================

pruebas = [

    # ------------------------------------------------
    # 1. COINCIDENCIAS BÁSICAS
    # ------------------------------------------------

    ("Roald Dahl", "Roald Dahl"),
    ("Jorge Luis Borges", "Jorge Luis Borges"),
    ("Gabriel García Márquez", "Gabriel García Márquez"),
    ("Mario Vargas Llosa", "Mario Vargas Llosa"),
    ("José Saramago", "José Saramago"),


    # ------------------------------------------------
    # 2. ORDEN APELLIDO, NOMBRE
    # ------------------------------------------------

    ("Roald Dahl", "Dahl, Roald"),
    ("Dahl, Roald", "Roald Dahl"),

    ("Jorge Luis Borges", "Borges, Jorge Luis"),
    ("Borges, Jorge Luis", "Jorge Luis Borges"),

    ("Gabriel García Márquez", "García Márquez, Gabriel"),
    ("Mario Vargas Llosa", "Vargas Llosa, Mario"),

    ("José Saramago", "Saramago, José"),


    # ------------------------------------------------
    # 3. TILDES Y ACENTOS
    # ------------------------------------------------

    ("Gabriel García Márquez", "Gabriel Garcia Marquez"),
    ("Julio Cortázar", "Julio Cortazar"),
    ("José Saramago", "Jose Saramago"),
    ("Borges, Jorge Luis", "Borges, Jorge Luis"),


    # ------------------------------------------------
    # 4. MAYÚSCULAS / MINÚSCULAS
    # ------------------------------------------------

    ("ROALD DAHL", "roald dahl"),
    ("Jorge Luis Borges", "JORGE LUIS BORGES"),
    ("GABRIEL GARCÍA MÁRQUEZ", "Gabriel García Márquez"),


    # ------------------------------------------------
    # 5. PUNTUACIÓN
    # ------------------------------------------------

    ("Jorge Luis Borges.", "Jorge Luis Borges"),
    ("Jorge Luis Borges", "Jorge Luis Borges."),
    ("Borges, Jorge Luis.", "Borges, Jorge Luis"),


    # ------------------------------------------------
    # 6. ERRORES TIPOGRÁFICOS
    # ------------------------------------------------

    ("Roald Dalh", "Roald Dahl"),
    ("Jorge Luis Borge", "Jorge Luis Borges"),
    ("Gabriel García Marquéz", "Gabriel García Márquez"),
    ("Julio Cortázar", "Julio Cortazar"),


    # ------------------------------------------------
    # 7. INICIALES
    # ------------------------------------------------

    ("J. L. Borges", "Jorge Luis Borges"),
    ("J.L. Borges", "Jorge Luis Borges"),
    ("Jorge L. Borges", "Jorge Luis Borges"),

    ("G. García Márquez", "Gabriel García Márquez"),
    ("García Márquez, G.", "Gabriel García Márquez"),

    ("Borges, J. L.", "Jorge Luis Borges"),
    ("Borges, J.", "Jorge Luis Borges"),


    # ------------------------------------------------
    # 8. SEGUNDO NOMBRE
    # ------------------------------------------------

    ("Gabriel García Márquez", "García Márquez, Gabriel José"),
    ("Gabriel José García Márquez", "García Márquez, Gabriel José"),

    ("Jorge Luis Borges", "Borges, Jorge Luis"),
    ("Jorge Francisco Isidoro Luis Borges", "Borges, Jorge Luis"),


    # ------------------------------------------------
    # 9. APELLIDOS COMPUESTOS
    # ------------------------------------------------

    ("Mario Vargas Llosa", "Vargas Llosa, Mario"),
    ("Vargas Llosa, Mario", "Mario Vargas Llosa"),

    ("Gabriel García Márquez", "García Márquez, Gabriel"),

    ("Miguel de Cervantes", "Cervantes, Miguel de"),
    ("Cervantes, Miguel de", "Miguel de Cervantes"),

    ("de Cervantes, Miguel", "Miguel de Cervantes"),


    # ------------------------------------------------
    # 10. AUTORES DIFERENTES
    # ------------------------------------------------

    ("Roald Dahl", "Julio Cortázar"),
    ("Jorge Luis Borges", "Gabriel García Márquez"),
    ("Mario Vargas Llosa", "José Saramago"),


    # ------------------------------------------------
    # 11. AUTORES PARECIDOS PERO DIFERENTES
    # ------------------------------------------------

    ("Jorge Luis Borges", "Jorge Luis Borge"),
    ("Gabriel García Márquez", "Gabriel García Marqués"),
    ("Mario Vargas Llosa", "Mario Vargas Losa"),


    # ------------------------------------------------
    # 12. MÚLTIPLES AUTORES
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Borges, Jorge Luis; Bioy Casares, Adolfo"
    ),

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Adolfo Bioy Casares; Jorge Luis Borges"
    ),

    (
        "Borges, Jorge Luis; Bioy Casares, Adolfo",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),

    (
        "Gabriel García Márquez; Mario Vargas Llosa",
        "García Márquez, Gabriel; Vargas Llosa, Mario"
    ),


    # ------------------------------------------------
    # 13. MÚLTIPLES AUTORES CON DIFERENCIAS
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges"
    ),

    (
        "Jorge Luis Borges",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges; Julio Cortázar"
    ),

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges; Adolfo Bioy Cazares"
    ),


    # ------------------------------------------------
    # 14. SEPARADORES DIFERENTES
    # ------------------------------------------------

    (
        "Jorge Luis Borges; Adolfo Bioy Casares",
        "Jorge Luis Borges, Adolfo Bioy Casares"
    ),

    (
        "Jorge Luis Borges / Adolfo Bioy Casares",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),

    (
        "Jorge Luis Borges y Adolfo Bioy Casares",
        "Jorge Luis Borges; Adolfo Bioy Casares"
    ),


    # ------------------------------------------------
    # 15. AUTORES CORPORATIVOS
    # ------------------------------------------------

    ("Organización Mundial de la Salud", "Organización Mundial de la Salud"),
    ("Organizacion Mundial de la Salud", "Organización Mundial de la Salud"),

    ("UNESCO", "UNESCO"),
    ("UNESCO", "United Nations Educational, Scientific and Cultural Organization"),

    ("Ministerio de Educación", "Ministerio de Educación"),
    ("Ministerio de Educación", "Ministerio de Educacion"),


    # ------------------------------------------------
    # 16. ESPACIOS EXTRA
    # ------------------------------------------------

    ("  Roald Dahl  ", "Roald Dahl"),
    ("Jorge   Luis   Borges", "Jorge Luis Borges"),

    (
        "Gabriel    García    Márquez",
        "García Márquez, Gabriel"
    ),


    # ------------------------------------------------
    # 17. DATOS VACÍOS
    # ------------------------------------------------

    ("", "Roald Dahl"),
    (None, "Roald Dahl"),

    ("Roald Dahl", ""),
    ("Roald Dahl", None),

    ("", ""),
    (None, None),
]


# ====================================================
# EJECUCIÓN
# ====================================================

print()
print("COMPARACIÓN DE AUTORES")
print("======================")

print()
print(f"Total de pruebas: {len(pruebas)}")


for numero, (autor_catalogo, autor_fuente) in enumerate(
    pruebas,
    start=1
):

    resultado = comparar_autor(
        autor_catalogo,
        autor_fuente
    )

    print()
    print("=" * 70)
    print(f"PRUEBA {numero}")

    print("-" * 70)

    print(f"Catálogo : {resultado['autor_catalogo']}")
    print(f"Fuente   : {resultado['autor_fuente']}")

    print(
        f"Normalizado catálogo : "
        f"{resultado['catalogo_normalizado']}"
    )

    print(
        f"Normalizado fuente   : "
        f"{resultado['fuente_normalizada']}"
    )

    print(
        f"Similitud            : "
        f"{resultado['similitud']}"
    )

    print(
        f"Resultado             : "
        f"{resultado['resultado']}"
    )


print()
print("=" * 70)
print("FIN DE LAS PRUEBAS")
print("=" * 70)