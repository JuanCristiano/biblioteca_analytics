from modulos.calidad_datos.informe import generar_informe


def resumen_ejemplo(**cambios):
    resumen = {
        "total_registros": 10,
        "errores": 1,
        "advertencias": 3,
        "registros_afectados": 2,
        "registros_sin_problemas": 8,
        "porcentaje_sin_problemas": 80.0,
        "problemas_por_regla": {"REGLA-001": 1, "REGLA-003": 3},
    }
    resumen.update(cambios)
    return resumen


def problema(registro, regla, nivel, campo, texto, sugerencia):
    return {
        "registro": registro,
        "regla": regla,
        "nivel": nivel,
        "campo": campo,
        "problema": texto,
        "sugerencia": sugerencia,
    }


def test_incluye_el_resumen_con_sus_cifras():
    lineas = generar_informe(resumen_ejemplo(), []).splitlines()

    assert "Registros analizados: 10" in lineas
    assert "Errores: 1" in lineas
    assert "Advertencias: 3" in lineas
    assert "Registros afectados: 2" in lineas
    assert "Registros sin problemas: 8" in lineas
    assert "Calidad sin alertas: 80.0%" in lineas


def test_muestra_el_porcentaje_con_un_decimal():
    informe = generar_informe(resumen_ejemplo(porcentaje_sin_problemas=33.3333), [])

    assert "Calidad sin alertas: 33.3%" in informe.splitlines()


def test_lista_los_problemas_por_regla():
    lineas = generar_informe(resumen_ejemplo(), []).splitlines()

    assert "REGLA-001: 1" in lineas
    assert "REGLA-003: 3" in lineas


def test_detalla_cada_problema_en_orden():
    errores = [
        problema("000008", "REGLA-001", "ERROR", "245",
                 "Título principal vacío", "Revisar y completar 245$a."),
        problema("000009", "REGLA-003", "ADVERTENCIA", "020",
                 "ISBN duplicado con el registro 000001", "Revisar la edición."),
    ]

    informe = generar_informe(resumen_ejemplo(), errores)
    lineas = informe.splitlines()

    assert "Registro: 000008" in lineas
    assert "Regla: REGLA-001" in lineas
    assert "Nivel: ERROR" in lineas
    assert "Campo: 245" in lineas
    assert "Problema: Título principal vacío" in lineas
    assert "Sugerencia: Revisar y completar 245$a." in lineas
    assert "Registro: 000009" in lineas
    assert informe.index("Registro: 000008") < informe.index("Registro: 000009")


def test_sin_problemas_no_hay_detalle_pero_si_las_secciones():
    informe = generar_informe(resumen_ejemplo(problemas_por_regla={}), [])

    assert "INFORME DE CALIDAD" in informe
    assert "DETALLE DE PROBLEMAS" in informe
    assert "Registro: " not in informe