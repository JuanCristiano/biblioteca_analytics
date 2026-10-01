from modulos.calidad_datos.informe_comparacion import generar_informe_comparacion


def auditoria(fecha, registros, afectados, sin_alertas, porcentaje):
    return {
        "fecha": fecha,
        "registros": str(registros),
        "registros_afectados": str(afectados),
        "registros_sin_alertas": str(sin_alertas),
        "porcentaje_sin_alertas": str(porcentaje),
    }


def comparacion_ejemplo(alertas, afectados, sin_alertas, porcentaje):
    return {
        "estado": "OK",
        "anterior": auditoria("2026-09-16 13:08:36", 200, 16, 184, 92.0),
        "actual": auditoria("2026-09-16 13:41:49", 200, 21, 179, 89.5),
        "diferencia_alertas": alertas,
        "diferencia_afectados": afectados,
        "diferencia_sin_alertas": sin_alertas,
        "diferencia_porcentaje": porcentaje,
    }


def test_si_no_hay_comparacion_devuelve_el_mensaje():
    comparacion = {"estado": "INSUFICIENTES", "mensaje": "Faltan auditorías."}

    assert generar_informe_comparacion(comparacion) == "Faltan auditorías."


def test_muestra_las_fechas_y_la_evolucion():
    lineas = generar_informe_comparacion(comparacion_ejemplo(5, 5, -5, -2.5)).splitlines()

    assert "Auditoría anterior: 2026-09-16 13:08:36" in lineas
    assert "Auditoría actual:   2026-09-16 13:41:49" in lineas
    assert "Registros analizados: 200 → 200" in lineas
    assert "Registros afectados: 16 → 21" in lineas
    assert "Registros sin alertas: 184 → 179" in lineas
    assert "Porcentaje sin alertas: 92.0% → 89.5%" in lineas


def test_cuando_la_calidad_empeora():
    lineas = generar_informe_comparacion(comparacion_ejemplo(5, 5, -5, -2.5)).splitlines()

    assert "Alertas: 5 más" in lineas
    assert "Registros afectados: 5 más" in lineas
    assert "Registros sin alertas: 5 menos" in lineas
    assert "Variación: -2.5 puntos porcentuales" in lineas


def test_cuando_la_calidad_mejora():
    lineas = generar_informe_comparacion(comparacion_ejemplo(-3, -3, 3, 1.5)).splitlines()

    assert "Alertas: 3 menos" in lineas
    assert "Registros afectados: 3 menos" in lineas
    assert "Registros sin alertas: 3 más" in lineas
    assert "Mejora: +1.5 puntos porcentuales" in lineas


def test_cuando_no_hay_cambios():
    lineas = generar_informe_comparacion(comparacion_ejemplo(0, 0, 0, 0.0)).splitlines()

    assert "Alertas: sin cambios" in lineas
    assert "Registros afectados: sin cambios" in lineas
    assert "Registros sin alertas: sin cambios" in lineas
    assert "Porcentaje sin alertas: sin cambios" in lineas