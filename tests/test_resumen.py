import pytest

from modulos.calidad_datos.resumen import resumir_resultados


def problema(registro, regla, nivel):
    return {"registro": registro, "regla": regla, "nivel": nivel}


def test_cuenta_errores_advertencias_y_registros_afectados():
    catalogo = [{} for _ in range(10)]
    errores = [
        problema("000008", "REGLA-001", "ERROR"),
        problema("000008", "REGLA-002", "ADVERTENCIA"),
        problema("000009", "REGLA-004", "ADVERTENCIA"),
        problema("000009", "REGLA-003", "ADVERTENCIA"),
    ]

    resumen = resumir_resultados(catalogo, errores)

    assert resumen["total_registros"] == 10
    assert resumen["errores"] == 1
    assert resumen["advertencias"] == 3
    assert resumen["registros_afectados"] == 2
    assert resumen["registros_sin_problemas"] == 8
    assert resumen["porcentaje_sin_problemas"] == pytest.approx(80.0)


def test_indicadores_por_regla():
    catalogo = [{} for _ in range(10)]
    errores = [
        problema("000008", "REGLA-001", "ERROR"),
        problema("000009", "REGLA-003", "ADVERTENCIA"),
    ]

    resumen = resumir_resultados(catalogo, errores)

    indicador = resumen["indicadores_por_regla"]["REGLA-001"]
    assert indicador["registros_afectados"] == 1
    assert indicador["porcentaje"] == pytest.approx(10.0)
    assert indicador["problemas"] == 1


def test_distingue_problemas_de_registros_afectados_en_una_regla():
    catalogo = [{} for _ in range(4)]
    errores = [
        problema("000001", "REGLA-002", "ADVERTENCIA"),
        problema("000001", "REGLA-002", "ADVERTENCIA"),
        problema("000002", "REGLA-002", "ADVERTENCIA"),
    ]

    resumen = resumir_resultados(catalogo, errores)

    indicador = resumen["indicadores_por_regla"]["REGLA-002"]
    assert resumen["problemas_por_regla"]["REGLA-002"] == 3
    assert indicador["problemas"] == 3
    assert indicador["registros_afectados"] == 2
    assert indicador["porcentaje"] == pytest.approx(50.0)


def test_catalogo_sin_errores_tiene_100_por_ciento_sin_problemas():
    resumen = resumir_resultados([{} for _ in range(5)], [])

    assert resumen["errores"] == 0
    assert resumen["advertencias"] == 0
    assert resumen["registros_afectados"] == 0
    assert resumen["porcentaje_sin_problemas"] == pytest.approx(100.0)


def test_catalogo_vacio_no_divide_por_cero():
    resumen = resumir_resultados([], [])

    assert resumen["total_registros"] == 0
    assert resumen["porcentaje_sin_problemas"] == 0