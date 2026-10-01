import pytest

from modulos.calidad_datos.comparar_auditorias import comparar_ultimas_auditorias

ENCABEZADO = (
    "fecha,registros,registros_afectados,registros_sin_alertas,"
    "porcentaje_sin_alertas,errores,advertencias\n"
)


def crear_historial(tmp_path, filas):
    ruta = tmp_path / "auditorias.csv"
    ruta.write_text(ENCABEZADO + "".join(f + "\n" for f in filas), encoding="utf-8")
    return ruta


def test_una_sola_auditoria_es_insuficiente(tmp_path):
    ruta = crear_historial(tmp_path, ["2026-09-16 13:08:36,200,16,184,92.0,4,12"])

    resultado = comparar_ultimas_auditorias(ruta)

    assert resultado["estado"] == "INSUFICIENTES"


def test_calcula_diferencias_entre_las_dos_ultimas(tmp_path):
    ruta = crear_historial(tmp_path, [
        "2026-09-16 13:08:36,200,16,184,92.0,4,12",
        "2026-09-16 13:41:49,200,21,179,89.5,4,17",
    ])

    resultado = comparar_ultimas_auditorias(ruta)

    assert resultado["estado"] == "OK"
    assert resultado["diferencia_alertas"] == 5
    assert resultado["diferencia_afectados"] == 5
    assert resultado["diferencia_sin_alertas"] == -5
    assert resultado["diferencia_porcentaje"] == pytest.approx(-2.5)


def test_con_tres_auditorias_compara_solo_las_ultimas_dos(tmp_path):
    ruta = crear_historial(tmp_path, [
        "2026-09-15 10:00:00,10,3,7,70.0,2,3",
        "2026-09-16 13:08:36,200,16,184,92.0,4,12",
        "2026-09-16 13:41:49,200,21,179,89.5,4,17",
    ])

    resultado = comparar_ultimas_auditorias(ruta)

    assert resultado["anterior"]["fecha"] == "2026-09-16 13:08:36"
    assert resultado["actual"]["fecha"] == "2026-09-16 13:41:49"