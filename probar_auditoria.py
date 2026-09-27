from auditoria import auditar_registros
from fuentes_bibliograficas import consultar_openlibrary


registros_catalogo = [

    {
        "isbn": "9780140328721",
        "titulo": "Fantastic Mr. Fox",
        "autor": "Roald Dahl",
        "editorial": "Puffin"
    },

    {
        "isbn": "9780140328721",
        "titulo": "Fantastic Mr. Foz",
        "autor": "Roald Dahl",
        "editorial": "Puffin"
    },

    {
        "isbn": "9780140328721",
        "titulo": "Fantastic Mr. Fox",
        "autor": "Dahl, Roald",
        "editorial": "Puffin"
    },

    {
        "isbn": "9999999999999",
        "titulo": "Libro inexistente",
        "autor": "Autor Desconocido",
        "editorial": "Editorial Desconocida"
    },

    {
        "isbn": "",
        "titulo": "Libro sin ISBN",
        "autor": "Autor Desconocido",
        "editorial": "Editorial Desconocida"
    }
]


# ----------------------------------------------------
# AUDITORÍA
# ----------------------------------------------------

resultados = auditar_registros(registros_catalogo)


print("AUDITORÍA BIBLIOGRÁFICA")
print("=======================")


for numero, resultado in enumerate(resultados, start=1):

    registro = resultado["registro_catalogo"]
    auditoria = resultado["resultado"]

    print()
    print(f"REGISTRO {numero}")
    print("-" * 30)

    print("Título:", registro.get("titulo"))
    print("Autor:", registro.get("autor"))
    print("Resultado:", auditoria.get("resultado"))
    print("ISBN:", auditoria.get("isbn"))
    print("Título coincide:", auditoria.get("titulo"))
    print("Autor coincide:", auditoria.get("autor"))
    print("Editorial coincide:", auditoria.get("editorial"))


# ----------------------------------------------------
# PRUEBA DIRECTA DE OPEN LIBRARY
# ----------------------------------------------------

print()
print("PRUEBA ISBN")
print("===========")

isbn = "9999999999999"

resultado_openlibrary = consultar_openlibrary(isbn)

print(resultado_openlibrary)