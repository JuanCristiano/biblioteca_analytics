def validar_titulo(registro):
    errores = []

    campo_245 = registro.get("245", [])

    if not campo_245:
        errores.append({
            "registro": registro.get("001"),
            "campo": "245",
            "subcampo": "a",
            "regla": "REGLA-001",
            "nivel": "ERROR",
            "problema": "Campo 245 ausente",
            "sugerencia": "Revisar y completar el título principal."
        })

        return errores

    titulo = campo_245[0].get("subcampos", {}).get("a", "").strip()

    if not titulo:
        errores.append({
            "registro": registro.get("001"),
            "campo": "245",
            "subcampo": "a",
            "regla": "REGLA-001",
            "nivel": "ERROR",
            "problema": "Título principal vacío",
            "sugerencia": "Revisar y completar 245$a."
        })

    return errores