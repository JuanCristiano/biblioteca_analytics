from comparar_titulos import comparar_titulo


# ----------------------------------------------------
# PRUEBAS
# ----------------------------------------------------

pruebas = [
    ("Fantastic Mr. Fox", "Fantastic Mr. Fox"),
    ("Fantastic Mr. Foz", "Fantastic Mr. Fox"),
    ("Fantastic Mr Fox", "Fantastic Mr. Fox"),
    ("El Aleph", "El Aleph"),
    ("El Aleph", "Rayuela"),
    ("Cien años de soledad", "Cien anos de soledad"),
    ("Don Quijote", "Don Quijote de la Mancha"),
    ("", "El Aleph"),
    (None, "El Aleph"),
    ("El amor en los tiempos del cólera", "El amor en los tiempos modernos"),
    ("Historia de la Argentina", "Historia de la literatura argentina"),
    ("Manual de economía", "Manual de economía política"),
    ("La casa de los espíritus", "La casa de Bernarda Alba"),
    ("Cien años de soledad", "Cien años de silencio"),
    ("Harry Potter", "Harry Potter y la piedra filosofal"),
]


# ----------------------------------------------------
# EJECUCIÓN
# ----------------------------------------------------

print("COMPARACIÓN DE TÍTULOS")
print("=======================")

for titulo_catalogo, titulo_fuente in pruebas:

    resultado = comparar_titulo(
        titulo_catalogo,
        titulo_fuente
    )

    print()
    print("-" * 60)

    print(f"Catálogo : {resultado['titulo_catalogo']}")
    print(f"Fuente   : {resultado['titulo_fuente']}")

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