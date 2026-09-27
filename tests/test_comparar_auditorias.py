from modulos.calidad_datos.comparar_auditorias import (
    comparar_ultimas_auditorias
)


RUTA_HISTORIAL = "data/historial/auditorias.csv"


resultado = comparar_ultimas_auditorias(
    RUTA_HISTORIAL
)


print(resultado)