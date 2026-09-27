from modulos.calidad_datos.comparar_auditorias import (
    comparar_ultimas_auditorias
)

from modulos.calidad_datos.informe_comparacion import (
    generar_informe_comparacion
)


RUTA_HISTORIAL = "data/historial/auditorias.csv"


comparacion = comparar_ultimas_auditorias(
    RUTA_HISTORIAL
)

informe = generar_informe_comparacion(
    comparacion
)

print(informe)