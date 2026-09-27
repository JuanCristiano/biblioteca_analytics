def validar_descripcion_fisica(registro):
    errores = []

    campo_300 = registro.get("300", [])

    if not campo_300:
        errores.append({
            "registro": registro.get("001"),
            "campo": "300",
            "subcampo": "",
            "regla": "REGLA-006",
            "nivel": "ADVERTENCIA",
            "problema": "Registro sin descripción física",
            "sugerencia": "Revisar si corresponde completar el campo 300."
        })

        return errores

    tiene_contenido = False

    for campo in campo_300:
        subcampos = campo.get("subcampos", {})

        if any(
            valor.strip()
            for valor in subcampos.values()
            if isinstance(valor, str)
        ):
            tiene_contenido = True
            break

    if not tiene_contenido:
        errores.append({
            "registro": registro.get("001"),
            "campo": "300",
            "subcampo": "",
            "regla": "REGLA-006",
            "nivel": "ADVERTENCIA",
            "problema": "Campo 300 presente pero sin contenido",
            "sugerencia": "Revisar y completar la descripción física."
        })

    return errores