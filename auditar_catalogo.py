
import os
from shutil import copyfile

from modulos.cargadores.cargar_json import cargar_catalogo_json
from modulos.cargadores.normalizar_csv import normalizar_catalogo_csv
from modulos.cargadores.convertir_a_marc import convertir_catalogo_a_marc
from modulos.cargadores.cargar_fuente_autores import cargar_fuente_autores

from modulos.calidad_datos.auditor import auditar_catalogo
from modulos.calidad_datos.resumen import resumir_resultados
from modulos.calidad_datos.informe import generar_informe
from modulos.calidad_datos.exportar_csv import exportar_errores_csv
from modulos.calidad_datos.exportar_resumen_csv import exportar_resumen_csv

from modulos.calidad_datos.historial import (
    guardar_auditoria,
    generar_id_auditoria,
    crear_directorio_auditoria
)

from modulos.calidad_datos.comparar_auditorias import (
    comparar_ultimas_auditorias
)

from modulos.calidad_datos.informe_comparacion import (
    generar_informe_comparacion
)


# ====================================================
# RUTAS
# ====================================================

RUTA_CATALOGO = (
    "data/raw/catalogo_marc_prueba_200.json"
)

RUTA_FUENTE_AUTORES = (
    "data/raw/fuente_autores_prueba_200.csv"
)

RUTA_INFORME = (
    "data/processed/informe_calidad.txt"
)

RUTA_CSV_ERRORES = (
    "data/processed/auditoria_catalogo.csv"
)

RUTA_CSV_RESUMEN = (
    "data/processed/resumen_calidad.csv"
)

RUTA_HISTORIAL = (
    "data/historial/auditorias.csv"
)

RUTA_COMPARACION = (
    "data/processed/comparacion_auditorias.txt"
)


# ====================================================
# CARGAR CATÁLOGO
# ====================================================

def cargar_catalogo(ruta):
    """
    Punto único de entrada de datos.

    Acepta:

    - JSON en estructura MARC
    - CSV con columnas variables

    Las reglas de calidad reciben siempre
    la misma estructura MARC.
    """

    extension = os.path.splitext(
        ruta
    )[1].lower()

    if extension == ".json":

        return cargar_catalogo_json(
            ruta
        )

    if extension == ".csv":

        resultado = normalizar_catalogo_csv(
            ruta
        )

        if resultado["columnas_desconocidas"]:

            print(
                "Columnas no reconocidas "
                "(se ignoraron):"
            )

            for columna in (
                resultado[
                    "columnas_desconocidas"
                ]
            ):

                print(
                    f"  - {columna}"
                )

            print()

        return convertir_catalogo_a_marc(
            resultado["catalogo"]
        )

    raise ValueError(
        f"Formato de archivo no soportado: "
        f"'{extension}'. "
        "Usá .json (MARC) o .csv."
    )


# ====================================================
# PROCESO PRINCIPAL
# ====================================================

def main():

    print(
        "========================================"
    )

    print(
        " AUDITORÍA DE CALIDAD DEL CATÁLOGO"
    )

    print(
        "========================================"
    )

    print()

    # ------------------------------------------------
    # CARGAR CATÁLOGO
    # ------------------------------------------------

    print(
        "Leyendo catálogo..."
    )

    catalogo = cargar_catalogo(
        RUTA_CATALOGO
    )

    print(
        f"Registros encontrados: "
        f"{len(catalogo)}"
    )

    print()

    # ------------------------------------------------
    # CARGAR FUENTE DE AUTORES
    # ------------------------------------------------

    print(
        "Leyendo fuente externa de autores..."
    )

    fuente_autores = cargar_fuente_autores(
        RUTA_FUENTE_AUTORES
    )

    print(
        f"Autores de fuente cargados: "
        f"{len(fuente_autores)}"
    )

    print()

    # ------------------------------------------------
    # EJECUTAR AUDITORÍA
    # ------------------------------------------------

    print(
        "Ejecutando auditoría..."
    )

    errores = auditar_catalogo(
        catalogo,
        fuente_autores
    )

    print(
        f"Alertas detectadas: "
        f"{len(errores)}"
    )

    # ------------------------------------------------
    # RESUMEN
    # ------------------------------------------------

    resumen = resumir_resultados(
        catalogo,
        errores
    )

    # ------------------------------------------------
    # INFORME
    # ------------------------------------------------

    informe = generar_informe(
        resumen,
        errores
    )

    with open(
        RUTA_INFORME,
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            informe
        )

    # ------------------------------------------------
    # EXPORTAR ERRORES
    # ------------------------------------------------

    exportar_errores_csv(
        errores,
        RUTA_CSV_ERRORES
    )

    # ------------------------------------------------
    # EXPORTAR RESUMEN
    # ------------------------------------------------

    exportar_resumen_csv(
        resumen[
            "indicadores_por_regla"
        ],
        RUTA_CSV_RESUMEN
    )

    # =================================================
    # CREAR SNAPSHOT
    # =================================================

    id_auditoria = generar_id_auditoria()

    ruta_historial_auditoria = (
        crear_directorio_auditoria(
            id_auditoria
        )
    )

    copyfile(
        RUTA_INFORME,
        os.path.join(
            ruta_historial_auditoria,
            "informe_calidad.txt"
        )
    )

    copyfile(
        RUTA_CSV_ERRORES,
        os.path.join(
            ruta_historial_auditoria,
            "auditoria_catalogo.csv"
        )
    )

    copyfile(
        RUTA_CSV_RESUMEN,
        os.path.join(
            ruta_historial_auditoria,
            "resumen_calidad.csv"
        )
    )

    # =================================================
    # GUARDAR HISTORIAL
    # =================================================

    guardar_auditoria(
        resumen,
        RUTA_HISTORIAL
    )

    # =================================================
    # COMPARAR AUDITORÍAS
    # =================================================

    comparacion = comparar_ultimas_auditorias(
        RUTA_HISTORIAL
    )

    informe_comparacion = (
        generar_informe_comparacion(
            comparacion
        )
    )

    with open(
        RUTA_COMPARACION,
        "w",
        encoding="utf-8"
    ) as archivo:

        archivo.write(
            informe_comparacion
        )

    # =================================================
    # RESULTADO FINAL
    # =================================================

    print()

    print(
        "Auditoría guardada."
    )

    print(
        f"ID de auditoría: "
        f"{id_auditoria}"
    )

    print(
        f"Snapshot: "
        f"{ruta_historial_auditoria}"
    )

    print()

    print(
        "Archivos generados:"
    )

    print(
        f"- {RUTA_INFORME}"
    )

    print(
        f"- {RUTA_CSV_ERRORES}"
    )

    print(
        f"- {RUTA_CSV_RESUMEN}"
    )

    print(
        f"- {RUTA_COMPARACION}"
    )

    print()

    print(
        "Auditoría finalizada correctamente."
    )


if __name__ == "__main__":
    main()
