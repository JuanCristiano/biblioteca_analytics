def generar_informe_comparacion(comparacion):

    if comparacion["estado"] != "OK":
        return comparacion["mensaje"]

    anterior = comparacion["anterior"]
    actual = comparacion["actual"]

    diferencia_alertas = comparacion["diferencia_alertas"]
    diferencia_afectados = comparacion["diferencia_afectados"]
    diferencia_sin_alertas = comparacion["diferencia_sin_alertas"]
    diferencia_porcentaje = comparacion["diferencia_porcentaje"]

    lineas = []

    lineas.append("=" * 50)
    lineas.append("COMPARACIÓN DE AUDITORÍAS")
    lineas.append("=" * 50)
    lineas.append("")

    lineas.append(
        f"Auditoría anterior: {anterior['fecha']}"
    )

    lineas.append(
        f"Auditoría actual:   {actual['fecha']}"
    )

    lineas.append("")

    lineas.append("-" * 50)
    lineas.append("EVOLUCIÓN")
    lineas.append("-" * 50)

    lineas.append(
        f"Registros analizados: "
        f"{anterior['registros']} → {actual['registros']}"
    )

    lineas.append(
        f"Registros afectados: "
        f"{anterior['registros_afectados']} → "
        f"{actual['registros_afectados']}"
    )

    lineas.append(
        f"Registros sin alertas: "
        f"{anterior['registros_sin_alertas']} → "
        f"{actual['registros_sin_alertas']}"
    )

    lineas.append(
        f"Porcentaje sin alertas: "
        f"{anterior['porcentaje_sin_alertas']}% → "
        f"{actual['porcentaje_sin_alertas']}%"
    )

    lineas.append("")

    lineas.append("-" * 50)
    lineas.append("CAMBIOS")
    lineas.append("-" * 50)

    if diferencia_alertas < 0:
        lineas.append(
            f"Alertas: {abs(diferencia_alertas)} menos"
        )
    elif diferencia_alertas > 0:
        lineas.append(
            f"Alertas: {diferencia_alertas} más"
        )
    else:
        lineas.append(
            "Alertas: sin cambios"
        )

    if diferencia_afectados < 0:
        lineas.append(
            f"Registros afectados: "
            f"{abs(diferencia_afectados)} menos"
        )
    elif diferencia_afectados > 0:
        lineas.append(
            f"Registros afectados: "
            f"{diferencia_afectados} más"
        )
    else:
        lineas.append(
            "Registros afectados: sin cambios"
        )

    if diferencia_sin_alertas > 0:
        lineas.append(
            f"Registros sin alertas: "
            f"{diferencia_sin_alertas} más"
        )
    elif diferencia_sin_alertas < 0:
        lineas.append(
            f"Registros sin alertas: "
            f"{abs(diferencia_sin_alertas)} menos"
        )
    else:
        lineas.append(
            "Registros sin alertas: sin cambios"
        )

    if diferencia_porcentaje > 0:
        lineas.append(
            f"Mejora: +{diferencia_porcentaje:.1f} "
            f"puntos porcentuales"
        )
    elif diferencia_porcentaje < 0:
        lineas.append(
            f"Variación: {diferencia_porcentaje:.1f} "
            f"puntos porcentuales"
        )
    else:
        lineas.append(
            "Porcentaje sin alertas: sin cambios"
        )

    lineas.append("")

    return "\n".join(lineas)