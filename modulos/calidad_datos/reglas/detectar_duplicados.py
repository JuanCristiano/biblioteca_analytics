def detectar_isbn_duplicados(catalogo):
    errores = []
    isbn_vistos = {}

    for registro in catalogo:
        id_registro = registro.get("001")

        for campo in registro.get("020", []):
            isbn = campo.get("subcampos", {}).get("a", "").strip()

            if not isbn:
                continue

            isbn_limpio = isbn.replace("-", "").replace(" ", "")

            if isbn_limpio in isbn_vistos:
                errores.append({
                    "registro": id_registro,
                    "campo": "020",
                    "subcampo": "a",
                    "regla": "REGLA-003",
                    "nivel": "ADVERTENCIA",
                    "problema": f"ISBN duplicado con el registro {isbn_vistos[isbn_limpio]}",
                    "sugerencia": "Revisar si ambos registros corresponden a la misma edición."
                })
            else:
                isbn_vistos[isbn_limpio] = id_registro

    return errores