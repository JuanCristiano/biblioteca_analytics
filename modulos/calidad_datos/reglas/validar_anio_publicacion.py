def validar_anio_publicacion(registro):
    errores = []

    publicaciones = registro.get("264")

    if not publicaciones:
        return errores

    tiene_anio = False

    for publicacion in publicaciones:
        subcampos = publicacion.get("subcampos", {})
        anio = subcampos.get("c", "")

        if anio and str(anio).strip():
            tiene_anio = True
            break

    if not tiene_anio:
        errores.append({
            "registro": registro.get("001"),
            "campo": "264",
            "subcampo": "c",
            "regla": "REGLA-005",
            "nivel": "ADVERTENCIA",
            "problema": "No se encontró año de publicación",
            "sugerencia": (
                "Revisar y completar el año de publicación "
                "si corresponde."
            )
        })

    return errores