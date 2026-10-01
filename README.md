# Biblioteca Analytics

> **English summary.** Biblioteca Analytics is a Python toolkit for auditing and cleaning bibliographic catalogs (MARC21-style records). It loads catalog data from JSON or CSV, applies data-quality rules (missing titles, invalid or duplicate ISBNs, missing publication data, broken links, author inconsistencies), writes quality reports, stores every audit in a history, and compares audits to measure whether a cleanup worked. Corrections are applied to a *copy* of the catalog and logged field by field (old value → new value), so the original data is never modified. It is a portfolio project by a professional librarian moving into data work: the demo runs on a synthetic 200-record catalog, the test suite has 603 automated tests, and the known limitations are listed openly [below](#limitaciones-conocidas).

---

**Proyecto de auditoría y control de calidad de datos bibliográficos con Python y metadatos MARC21.**

Biblioteca Analytics explora cómo la programación y el análisis de datos pueden aplicarse a problemas reales de gestión bibliotecaria, especialmente en procesos de **migración, normalización, limpieza y control de calidad de catálogos**.

---

## Resultados de la demo

Sobre un catálogo sintético de 200 registros:

| Indicador                        | Resultado |
| -------------------------------- | --------: |
| Registros analizados             |       200 |
| Alertas iniciales                |        21 |
| Correcciones aplicadas           |         3 |
| Alertas posteriores              |        18 |
| Reducción de alertas             |         3 |
| Mejora relativa de alertas       |    14,3 % |

> **Cómo leer este resultado.** El catálogo es sintético y el generador (`scripts/generar_catalogo_200.py`) quita a propósito el año del registro 36, el subtítulo del 39 y las páginas del 48. Las tres correcciones de la demo devuelven esos valores, así que el 14,3 % muestra que el flujo *detecta, corrige, registra y vuelve a medir*, no una mejora sobre datos reales. Se puede reproducir con:
>
> ```bash
> python -m pytest tests/test_aplicar_correcciones.py -k 21_a_18
> ```

Cada corrección queda registrada con el registro, el campo MARC21, el subcampo, el valor anterior y el valor nuevo.

---

## Cómo probarlo

```bash
git clone https://github.com/JuanCristiano/biblioteca_analytics.git
cd biblioteca_analytics

python -m pip install -r requirements.txt
python auditar_catalogo.py
```

En Windows, si `python` no funciona, usar `py` en su lugar. Desarrollado y probado con Python 3.14; la única dependencia externa es `requests`.

El programa lee el catálogo de prueba de `data/raw/` y genera:

* `data/processed/informe_calidad.txt`: informe legible con el detalle de cada problema;
* `data/processed/auditoria_catalogo.csv`: una fila por alerta;
* `data/processed/resumen_calidad.csv`: indicadores por regla;
* `data/processed/comparacion_auditorias.txt`: diferencias con la auditoría anterior;
* `data/historial/<fecha_hora>/`: copia de cada auditoría, para compararlas más adelante.

Las carpetas `data/processed/` y `data/historial/` se crean al ejecutar y no se guardan en git.

**Tests:**

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

**Regenerar los datos de prueba** (no usa azar: produce siempre los mismos archivos):

```bash
python scripts/generar_catalogo_200.py
```

---

## Problema a resolver

Los catálogos bibliográficos acumulan errores e inconsistencias, sobre todo cuando los datos vienen de distintos sistemas, migraciones o cargas manuales:

* títulos incompletos o ausentes;
* autores ausentes o escritos de formas distintas;
* ISBN inválidos o duplicados;
* fechas de publicación y descripciones físicas faltantes;
* enlaces incorrectos;
* archivos CSV con columnas y estructuras diferentes.

Esto afecta la recuperación de la información y aumenta el trabajo de mantener un catálogo de calidad.

---

## Flujo general

```text
Catálogo (JSON MARC o CSV)
          |
          v
Carga; en CSV: detección de separador,
mapeo de columnas y conversión a estructura MARC
          |
          v
Reglas de calidad + comparación de autores con una fuente externa
          |
          v
Resumen e indicadores por regla
          |
          v
Informes (TXT y CSV) + copia en el historial de auditorías
          |
          v
Comparación con la auditoría anterior
```

Por separado, como módulos independientes:

```text
Lista de correcciones --> copia corregida del catálogo + historial de cambios --> nueva auditoría

Registros con ISBN --> consulta a Open Library --> comparación por campo
```

---

## Funcionalidades

### Reglas de calidad

Validaciones sobre título, subtítulo, autor principal, ISBN, año de publicación, datos de publicación, descripción física, enlaces y extensión, más detección de ISBN duplicados. Viven en `modulos/calidad_datos/reglas/`. Cada alerta indica registro, campo, subcampo, regla, nivel (`ERROR` o `ADVERTENCIA`), problema y sugerencia.

### Identificadores

Validación de ISBN-10, ISBN-13 e ISSN: formato y dígito de control, tolerando guiones y espacios.

### Comparación de autores y títulos

Resuelve un problema habitual: una misma persona escrita de formas distintas (`Dahl, Roald` / `Roald Dahl`). La comparación ignora mayúsculas, tildes, puntuación y el orden *Apellido, Nombre*, y acepta varios autores separados por `;`, `/` o `y`. El resultado se gradúa:

```text
COINCIDE  ->  POSIBLE COINCIDENCIA (similitud >= 0,85)  ->  NO COINCIDE  (+ NO DISPONIBLE si falta un dato)
```

Para autores con varios nombres, además informa faltantes, adicionales y el motivo (`AUTOR_FALTANTE`, `AUTOR_ADICIONAL`, `POSIBLE_VARIANTE`, etc.). En la demo, los autores del catálogo se comparan contra un archivo CSV que simula una fuente externa.

### Carga de CSV con columnas variables

Detecta el separador (`,`, `;`, tabulador o `|`), reconoce columnas por nombre o sinónimo (`Responsable`, `Autor principal` → `autor`), informa las columnas desconocidas y califica el mapeo con confianza `ALTA`, `MEDIA` o `BAJA`.

### Correcciones y trazabilidad

`aplicar_correcciones` trabaja sobre una copia: el catálogo original nunca se modifica. Devuelve el catálogo corregido y un historial con lo aplicado y lo rechazado (registro no encontrado, campo o subcampo sin informar).

### Historial y comparación de auditorías

Cada ejecución guarda un resumen y una copia de los informes. La comparación entre las dos últimas auditorías indica cuántas alertas y registros afectados aparecieron o desaparecieron y cuánto cambió el porcentaje de registros sin alertas.

### Fuentes externas

`modulos/fuentes/` consulta **Open Library** y **Google Books** por ISBN y compara título, autor y editorial con el registro del catálogo. Todavía **no está conectado** a `auditar_catalogo.py`.

---

## Estructura del proyecto

```text
biblioteca_analytics/
├── auditar_catalogo.py        # punto de entrada: auditoría completa
├── identificadores.py
├── requirements.txt
├── requirements-dev.txt
├── LICENSE
├── data/
│   ├── raw/                   # catálogos y fuentes de prueba (sintéticos)
│   └── generator/
│       └── leer_catalogo.py
├── docs/
│   ├── diccionario_funciones.md
│   ├── modelo_marc21.md
│   └── ejemplo_auditoria.md
├── modulos/
│   ├── calidad_datos/         # auditor, reglas, informes, historial, correcciones
│   │   └── reglas/
│   ├── cargadores/            # JSON, CSV, mapeo de columnas, conversión a MARC
│   ├── comparacion/           # similitud de texto, autores, títulos, registros
│   ├── fuentes/               # Open Library y Google Books
│   └── normalizacion/
├── scripts/
│   └── generar_catalogo_200.py
└── tests/                     # 603 tests con pytest
```

---

## Tests

La suite tiene **603 tests** en 23 archivos. Las funciones que usan archivos trabajan sobre carpetas temporales, y las que consultan internet se prueban con respuestas simuladas, así que los tests no dependen de la red ni de archivos generados. Las limitaciones conocidas del código quedan documentadas como tests llamados `test_limitacion_*`:

```bash
python -m pytest -k limitacion
```

---

## Limitaciones conocidas

* **Solo datos sintéticos.** No se probó todavía con un catálogo real.
* **Rutas fijas.** `auditar_catalogo.py` lee siempre el catálogo de prueba de 200 registros; para usar otro hay que cambiar las rutas del código.
* **Codificación de los CSV.** Se leen como UTF-8. Un CSV guardado como "CSV (delimitado por comas)" de Excel en español (ANSI) produce un error. La función `cargar_catalogo_csv` tampoco detecta el separador; `normalizar_catalogo_csv` sí.
* **Mapeo de columnas.** No reconoce la columna de materias ni `ISBN-10`, y dos columnas que apuntan al mismo campo se pisan entre sí.
* **Nombres abreviados.** `J. L. Borges` no se reconoce como `Jorge Luis Borges`.
* **Fuentes externas.** Un fallo de conexión con Open Library se informa como `NO ENCONTRADO`, sin distinguirlo de un ISBN inexistente.
* **Funciones repetidas.** Algunas funciones de normalización existen en más de un módulo, con comportamientos parecidos pero no idénticos; falta unificarlas.

---

## Próximos pasos

* Probar con un catálogo real anonimizado y documentar los resultados.
* Aceptar el archivo de entrada por línea de comandos.
* Guardar los resultados de las auditorías en una base de datos SQL y escribir consultas de indicadores de calidad.
* Dashboard en Power BI sobre esos indicadores.
* Conectar la comparación con Open Library al flujo de auditoría.
* Unificar las funciones de normalización repetidas.

---

## Contexto bibliotecológico

El proyecto surge de la experiencia profesional en gestión de bibliotecas, catalogación, repositorios digitales (Koha, DSpace) y metadatos bibliográficos. La idea es explorar cómo Python puede complementar el trabajo bibliotecario en procesos de **migración, limpieza y control de calidad de catálogos**.

---

## Autor

**Juan Gabriel Cristiano**, bibliotecario profesional.

Experiencia en bibliotecas, repositorios digitales, gestión de información y coordinación de equipos. Actualmente desarrollando proyectos de análisis de datos con Python; SQL y Power BI figuran como próximos pasos.

## Estado del proyecto

**En desarrollo.** Es un proyecto de portfolio: las funcionalidades se incorporan a medida que se desarrollan y se prueban.

## Licencia

[MIT](LICENSE)
