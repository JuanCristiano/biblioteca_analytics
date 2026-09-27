def validar_isbn(registro):
    errores = []

    campos_020 = registro.get("020", [])

    if not campos_020:
        errores.append({
            "registro": registro.get("001"),
            "campo": "020",
            "subcampo": "a",
            "regla": "REGLA-002",
            "nivel": "ADVERTENCIA",
            "problema": "Registro sin ISBN",
            "sugerencia": "Verificar si la publicación posee ISBN."
        })

        return errores

    for campo in campos_020:

        isbn = campo.get("subcampos", {}).get("a", "").strip()

        if not isbn:
            errores.append({
                "registro": registro.get("001"),
                "campo": "020",
                "subcampo": "a",
                "regla": "REGLA-002",
                "nivel": "ERROR",
                "problema": "ISBN vacío",
                "sugerencia": "Revisar y completar 020$a."
            })

            continue

        isbn_limpio = isbn.replace("-", "").replace(" ", "")

        if not isbn_limpio.isdigit():
            errores.append({
                "registro": registro.get("001"),
                "campo": "020",
                "subcampo": "a",
                "regla": "REGLA-002",
                "nivel": "ERROR",
                "problema": "ISBN contiene caracteres no numéricos",
                "sugerencia": "Revisar el formato del ISBN."
            })

            continue

        if len(isbn_limpio) != 13:
            errores.append({
                "registro": registro.get("001"),
                "campo": "020",
                "subcampo": "a",
                "regla": "REGLA-002",
                "nivel": "ERROR",
                "problema": "El ISBN no tiene 13 dígitos",
                "sugerencia": "Verificar si corresponde a un ISBN-13."
            })

            continue

        suma = 0

        for posicion, digito in enumerate(isbn_limpio[:12]):
            if posicion % 2 == 0:
                suma += int(digito)
            else:
                suma += int(digito) * 3

        digito_control = (10 - (suma % 10)) % 10

        if digito_control != int(isbn_limpio[-1]):
            errores.append({
                "registro": registro.get("001"),
                "campo": "020",
                "subcampo": "a",
                "regla": "REGLA-002",
                "nivel": "ERROR",
                "problema": "Dígito de control del ISBN-13 incorrecto",
                "sugerencia": "Revisar el ISBN registrado."
            })

    return errores