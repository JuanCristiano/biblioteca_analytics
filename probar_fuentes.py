from fuentes_bibliograficas import (
    consultar_openlibrary,
    consultar_google_books
)


isbn = "9780140328721"


print("CONSULTA BIBLIOGRÁFICA")
print("======================")
print()

print("OPEN LIBRARY")
print("------------")

resultado_openlibrary = consultar_openlibrary(isbn)

for clave, valor in resultado_openlibrary.items():
    print(f"{clave}: {valor}")

print()
print("GOOGLE BOOKS")
print("------------")

resultado_google = consultar_google_books(isbn)

for clave, valor in resultado_google.items():
    print(f"{clave}: {valor}")