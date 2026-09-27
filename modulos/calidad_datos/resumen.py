from collections import Counter


def resumir_resultados(catalogo, errores):
    total_registros = len(catalogo)

    cantidad_errores = sum(
        1 for error in errores
        if error["nivel"] == "ERROR"
    )

    cantidad_advertencias = sum(
        1 for error in errores
        if error["nivel"] == "ADVERTENCIA"
    )

    registros_afectados = {
        error["registro"]
        for error in errores
    }

    cantidad_registros_afectados = len(registros_afectados)

    registros_sin_problemas = (
        total_registros - cantidad_registros_afectados
    )

    if total_registros > 0:
        porcentaje_sin_problemas = (
            registros_sin_problemas / total_registros
        ) * 100
    else:
        porcentaje_sin_problemas = 0

    problemas_por_regla = Counter(
        error["regla"]
        for error in errores
    )

    registros_por_regla = {}

    for error in errores:
        regla = error["regla"]

        if regla not in registros_por_regla:
            registros_por_regla[regla] = set()

        registros_por_regla[regla].add(
            error["registro"]
        )

    indicadores_por_regla = {}

    for regla, registros in registros_por_regla.items():
        cantidad = len(registros)

        if total_registros > 0:
            porcentaje = (
                cantidad / total_registros
            ) * 100
        else:
            porcentaje = 0

        indicadores_por_regla[regla] = {
            "registros_afectados": cantidad,
            "porcentaje": porcentaje,
            "problemas": problemas_por_regla[regla]
        }

    return {
        "total_registros": total_registros,
        "errores": cantidad_errores,
        "advertencias": cantidad_advertencias,
        "registros_afectados": cantidad_registros_afectados,
        "registros_sin_problemas": registros_sin_problemas,
        "porcentaje_sin_problemas": porcentaje_sin_problemas,
        "problemas_por_regla": dict(problemas_por_regla),
        "indicadores_por_regla": indicadores_por_regla
    }