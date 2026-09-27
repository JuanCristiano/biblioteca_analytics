from modulos.cargadores.cargar_json import cargar_catalogo_json
from modulos.calidad_datos.auditor import auditar_catalogo
from modulos.calidad_datos.aplicar_correcciones import aplicar_correcciones
from modulos.cargadores.cargar_fuente_autores import cargar_fuente_autores

RUTA_CATALOGO = "data/raw/catalogo_marc_prueba_200.json"

RUTA_FUENTE_AUTORES = "data/raw/fuente_autores_prueba_200.csv"

# ====================================================
# CARGAR CATÁLOGO
# ====================================================

catalogo = cargar_catalogo_json(
    RUTA_CATALOGO
)

fuente_autores = cargar_fuente_autores(
    RUTA_FUENTE_AUTORES
)

# ====================================================
# AUDITORÍA ANTES DE CORREGIR
# ====================================================

errores_antes = auditar_catalogo(
    catalogo,
    fuente_autores
)


# ====================================================
# CORRECCIONES
# ====================================================

correcciones = [

    {
        "001": "000036",
        "campo": "264",
        "subcampo": "c",
        "valor_nuevo": "2020",
        "motivo": "Completar año de publicación"
    },

    {
        "001": "000039",
        "campo": "245",
        "subcampo": "b",
        "valor_nuevo": "Una introducción",
        "motivo": "Completar subtítulo"
    },

    {
        "001": "000048",
        "campo": "300",
        "subcampo": "a",
        "valor_nuevo": "245 páginas",
        "motivo": "Completar extensión física"
    }

]


# ====================================================
# APLICAR CORRECCIONES
# ====================================================

catalogo_corregido, historial = aplicar_correcciones(
    catalogo,
    correcciones
)



# ====================================================
# AUDITORÍA DESPUÉS DE CORREGIR
# ====================================================

errores_despues = auditar_catalogo(
    catalogo_corregido,
    fuente_autores
)


# ====================================================
# RESULTADOS
# ====================================================

print("=" * 50)
print("LIMPIEZA Y CORRECCIÓN DEL CATÁLOGO")
print("=" * 50)

print()

print(
    "Registros analizados:",
    len(catalogo)
)

print(
    "Alertas antes de corregir:",
    len(errores_antes)
)

print(
    "Correcciones aplicadas:",
    len([
        item
        for item in historial
        if item.get("resultado") == "APLICADA"
    ])
)

print(
    "Alertas después de corregir:",
    len(errores_despues)
)

print()

print("-" * 50)
print("HISTORIAL DE CORRECCIONES")
print("-" * 50)

for correccion in historial:
    print(
        f"{correccion['001']} | "
        f"{correccion['campo']}${correccion['subcampo']} | "
        f"{correccion.get('valor_anterior', '')} → "
        f"{correccion.get('valor_nuevo', '')} | "
        f"{correccion['resultado']} | "
        f"{correccion.get('motivo', '')}"
    )

print()

print("-" * 50)
print("COMPARACIÓN")
print("-" * 50)

mejora = len(errores_antes) - len(errores_despues)

print(
    "Reducción de alertas:",
    mejora
)

if len(errores_antes) > 0:

    porcentaje = (
        mejora / len(errores_antes)
    ) * 100

    print(
        f"Mejora relativa: {porcentaje:.1f}%"
    )

print()

print("=" * 50)
print("PRUEBA FINALIZADA")
print("=" * 50)