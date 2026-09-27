def validar_subtitulo(registro):
    errores = []

    titulos = registro.get("245")

    if not titulos:
        return errores

    for titulo in titulos:
        subcampos = titulo.get("subcampos", {})

        if "b" not in subcampos:
            continue

        subtitulo = subcampos.get("b", "")

        if subtitulo is None or not str(subtitulo).strip():
            errores.append({
                "registro": registro.get("001"),
                "campo": "245",
                "subcampo": "b",
                "regla": "REGLA-008",
                "nivel": "ADVERTENCIA",
                "problema": "El subcampo 245$b está vacío",
                "sugerencia": (
                    "Revisar si corresponde eliminar el subcampo "
                    "o completar la información del subtítulo."
                )
            })

    return errores