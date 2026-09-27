import copy


def aplicar_correcciones(catalogo, correcciones):
    """
    Aplica correcciones manuales sobre una copia del catálogo.

    No modifica el catálogo original.

    Cada corrección debe contener:

        001
        campo
        subcampo
        valor_nuevo
        motivo

    Ejemplo:

        {
            "001": "000008",
            "campo": "245",
            "subcampo": "a",
            "valor_nuevo": "Título corregido",
            "motivo": "Corrección manual"
        }

    Devuelve:

        catalogo_corregido
        historial_correcciones
    """

    catalogo_corregido = copy.deepcopy(catalogo)

    historial_correcciones = []

    registros_por_id = {
        registro.get("001"): registro
        for registro in catalogo_corregido
    }

    for correccion in correcciones:

        identificador = str(
            correccion.get("001", "")
        ).strip()

        campo = str(
            correccion.get("campo", "")
        ).strip()

        subcampo = str(
            correccion.get("subcampo", "")
        ).strip()

        valor_nuevo = correccion.get(
            "valor_nuevo",
            ""
        )

        motivo = str(
            correccion.get("motivo", "")
        ).strip()

        registro = registros_por_id.get(
            identificador
        )

        if registro is None:
            historial_correcciones.append({
                "001": identificador,
                "campo": campo,
                "subcampo": subcampo,
                "resultado": "NO APLICADA",
                "motivo": "Registro no encontrado"
            })

            continue

        if not campo:
            historial_correcciones.append({
                "001": identificador,
                "campo": "",
                "subcampo": subcampo,
                "resultado": "NO APLICADA",
                "motivo": "Campo MARC no informado"
            })

            continue

        if not subcampo:
            historial_correcciones.append({
                "001": identificador,
                "campo": campo,
                "subcampo": "",
                "resultado": "NO APLICADA",
                "motivo": "Subcampo no informado"
            })

            continue

        campos = registro.setdefault(
            campo,
            []
        )

        if not campos:
            campos.append({
                "subcampos": {}
            })

        aplicado = False

        for elemento in campos:

            subcampos = elemento.setdefault(
                "subcampos",
                {}
            )

            if subcampo in subcampos:

                valor_anterior = subcampos[
                    subcampo
                ]

                subcampos[subcampo] = valor_nuevo

                historial_correcciones.append({
                    "001": identificador,
                    "campo": campo,
                    "subcampo": subcampo,
                    "valor_anterior": valor_anterior,
                    "valor_nuevo": valor_nuevo,
                    "resultado": "APLICADA",
                    "motivo": motivo
                })

                aplicado = True
                break

        if not aplicado:

            campos[0]["subcampos"][
                subcampo
            ] = valor_nuevo

            historial_correcciones.append({
                "001": identificador,
                "campo": campo,
                "subcampo": subcampo,
                "valor_anterior": "",
                "valor_nuevo": valor_nuevo,
                "resultado": "APLICADA",
                "motivo": motivo
            })

    return (
        catalogo_corregido,
        historial_correcciones
    )