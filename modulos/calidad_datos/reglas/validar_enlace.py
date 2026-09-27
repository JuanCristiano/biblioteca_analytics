from urllib.parse import urlparse


def validar_enlace(registro):
    errores = []

    enlaces = registro.get("856")

    if not enlaces:
        return errores

    for enlace in enlaces:
        subcampos = enlace.get("subcampos", {})
        url = subcampos.get("u", "")

        if not url or not str(url).strip():
            errores.append({
                "registro": registro.get("001"),
                "campo": "856",
                "subcampo": "u",
                "regla": "REGLA-007",
                "nivel": "ADVERTENCIA",
                "problema": "El campo 856 no contiene una URL",
                "sugerencia": (
                    "Revisar y completar el enlace "
                    "del recurso electrónico."
                )
            })

            continue

        url = str(url).strip()

        try:
            resultado = urlparse(url)

            if resultado.scheme not in ("http", "https"):
                errores.append({
                    "registro": registro.get("001"),
                    "campo": "856",
                    "subcampo": "u",
                    "regla": "REGLA-007",
                    "nivel": "ADVERTENCIA",
                    "problema": "La URL no utiliza HTTP o HTTPS",
                    "sugerencia": (
                        "Revisar que el enlace tenga una URL válida "
                        "con protocolo HTTP o HTTPS."
                    )
                })

            elif not resultado.netloc:
                errores.append({
                    "registro": registro.get("001"),
                    "campo": "856",
                    "subcampo": "u",
                    "regla": "REGLA-007",
                    "nivel": "ADVERTENCIA",
                    "problema": "La URL no contiene un dominio válido",
                    "sugerencia": (
                        "Revisar y corregir la URL del recurso."
                    )
                })

        except ValueError:
            errores.append({
                "registro": registro.get("001"),
                "campo": "856",
                "subcampo": "u",
                "regla": "REGLA-007",
                "nivel": "ADVERTENCIA",
                "problema": "No fue posible interpretar la URL",
                "sugerencia": (
                    "Revisar y corregir el enlace."
                )
            })

    return errores