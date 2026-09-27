def generar_informe(resumen, errores):
    lineas = []

    lineas.append("=" * 50)
    lineas.append("INFORME DE CALIDAD DEL CATÁLOGO")
    lineas.append("=" * 50)
    lineas.append("")

    lineas.append(
        f"Registros analizados: {resumen['total_registros']}"
    )

    lineas.append(
        f"Errores: {resumen['errores']}"
    )

    lineas.append(
        f"Advertencias: {resumen['advertencias']}"
    )

    lineas.append(
        f"Registros afectados: {resumen['registros_afectados']}"
    )

    lineas.append(
        f"Registros sin problemas: {resumen['registros_sin_problemas']}"
    )

    lineas.append(
    f"Calidad sin alertas: {resumen['porcentaje_sin_problemas']:.1f}%"
)

    lineas.append("")
    lineas.append("-" * 50)
    lineas.append("PROBLEMAS POR REGLA")
    lineas.append("-" * 50)

    for regla, cantidad in resumen["problemas_por_regla"].items():
        lineas.append(
            f"{regla}: {cantidad}"
        )

    lineas.append("")
    lineas.append("-" * 50)
    lineas.append("DETALLE DE PROBLEMAS")
    lineas.append("-" * 50)

    for error in errores:
        lineas.append("")
        lineas.append(
            f"Registro: {error['registro']}"
        )
        lineas.append(
            f"Regla: {error['regla']}"
        )
        lineas.append(
            f"Nivel: {error['nivel']}"
        )
        lineas.append(
            f"Campo: {error['campo']}"
        )
        lineas.append(
            f"Problema: {error['problema']}"
        )
        lineas.append(
            f"Sugerencia: {error['sugerencia']}"
        )

    return "\n".join(lineas)