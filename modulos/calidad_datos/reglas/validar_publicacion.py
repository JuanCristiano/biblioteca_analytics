def validar_publicacion(registro):
    errores = []

    tiene_260 = bool(registro.get("260"))
    tiene_264 = bool(registro.get("264"))

    if not tiene_260 and not tiene_264:
        errores.append({
            "registro": registro.get("001"),
            "campo": "260/264",
            "subcampo": "",
            "regla": "REGLA-005",
            "nivel": "ADVERTENCIA",
            "problema": "No se encontró información de publicación",
            "sugerencia": "Revisar si corresponde completar el campo 260 o 264."
        })

    return errores