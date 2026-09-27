def validar_autor_principal(registro):
    errores = []

    campos_autor = ["100", "110", "111"]

    tiene_autor = any(
        registro.get(campo)
        for campo in campos_autor
    )

    if not tiene_autor:
        errores.append({
            "registro": registro.get("001"),
            "campo": "100/110/111",
            "subcampo": "",
            "regla": "REGLA-004",
            "nivel": "ADVERTENCIA",
            "problema": "No se encontró acceso principal de autor",
            "sugerencia": "Revisar si corresponde completar 100, 110 o 111."
        })

    return errores