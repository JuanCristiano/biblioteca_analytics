def validar_extension(registro):
    errores = []

    descripciones = registro.get("300")

    if not descripciones:
        return errores

    tiene_extension = False

    for descripcion in descripciones:
        subcampos = descripcion.get("subcampos", {})
        extension = subcampos.get("a", "")

        if extension and str(extension).strip():
            tiene_extension = True
            break

    if not tiene_extension:
        errores.append({
            "registro": registro.get("001"),
            "campo": "300",
            "subcampo": "a",
            "regla": "REGLA-006",
            "nivel": "ADVERTENCIA",
            "problema": (
                "No se encontró información de extensión "
                "en la descripción física"
            ),
            "sugerencia": (
                "Revisar y completar la extensión física "
                "de la publicación."
            )
        })

    return errores