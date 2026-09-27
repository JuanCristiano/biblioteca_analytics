# Ejemplo de auditoría bibliográfica

Este documento muestra un ejemplo del funcionamiento de `biblioteca_analytics` sobre datos bibliográficos de prueba.

El objetivo es ilustrar cómo el proyecto puede detectar inconsistencias, contrastar información bibliográfica y registrar correcciones realizadas sobre un catálogo.

---

## 1. Auditoría bibliográfica con fuente externa

El proyecto permite contrastar determinados registros con fuentes bibliográficas externas.

En esta prueba se utilizó **Open Library** como fuente de comparación.

### Registros analizados

| Registro | Título            | Autor             | Resultado     |
| -------- | ----------------- | ----------------- | ------------- |
| 1        | Fantastic Mr. Fox | Roald Dahl        | No encontrado |
| 2        | Fantastic Mr. Foz | Roald Dahl        | No encontrado |
| 3        | Fantastic Mr. Fox | Dahl, Roald       | No encontrado |
| 4        | Libro inexistente | Autor Desconocido | No encontrado |
| 5        | Libro sin ISBN    | Autor Desconocido | Sin ISBN      |

La prueba también contempla la consulta mediante ISBN.

Para un ISBN inexistente utilizado deliberadamente en los datos de prueba, Open Library respondió con un error HTTP 404. El proyecto registra este resultado como parte del proceso de auditoría en lugar de asumir que el registro bibliográfico es correcto.

### ¿Qué permite evaluar esta etapa?

* Disponibilidad de información bibliográfica externa.
* Existencia o ausencia de registros en una fuente de referencia.
* Comparación de títulos.
* Comparación de autores.
* Comparación de editoriales cuando existe información disponible.
* Identificación de registros sin ISBN.
* Manejo de respuestas y errores provenientes de fuentes externas.

---

# 2. Limpieza y corrección de un catálogo

La segunda prueba se realizó sobre un catálogo sintético de **200 registros**.

El proceso permite analizar el catálogo, identificar alertas y aplicar determinadas correcciones automáticas.

### Resultado antes y después

| Indicador                   | Resultado |
| --------------------------- | --------: |
| Registros analizados        |       200 |
| Alertas antes de corregir   |        21 |
| Correcciones aplicadas      |         3 |
| Alertas después de corregir |        18 |
| Reducción de alertas        |         3 |
| Mejora relativa             |    14,3 % |

La cantidad de alertas pasó de **21 a 18**, luego de aplicar tres correcciones.

---

## 3. Correcciones realizadas

El sistema registra cada modificación realizada, incluyendo el registro afectado, campo MARC21, valor anterior, valor nuevo y descripción de la corrección.

| Registro | Campo | Valor anterior | Valor nuevo      | Corrección                   |
| -------- | ----- | -------------- | ---------------- | ---------------------------- |
| 000036   | 264$c | vacío          | 2020             | Completar año de publicación |
| 000039   | 245$b | vacío          | Una introducción | Completar subtítulo          |
| 000048   | 300$a | vacío          | 245 páginas      | Completar extensión física   |

Esto permite mantener trazabilidad sobre las modificaciones realizadas durante el proceso de limpieza.

---

## 4. Comparación del resultado

```text
ANTES DE LA CORRECCIÓN
----------------------
Registros: 200
Alertas:   21

          ↓
     CORRECCIONES
          ↓

DESPUÉS DE LA CORRECCIÓN
------------------------
Registros: 200
Alertas:   18

Reducción: 3 alertas
Mejora relativa: 14,3 %
```

La comparación entre auditorías permite observar si las intervenciones sobre el catálogo producen una reducción de los problemas detectados.

---

## 5. Historial y trazabilidad

Las correcciones no se realizan simplemente sobre el dato original.

El proyecto registra información sobre:

* identificador del registro;
* campo MARC21;
* subcampo;
* valor anterior;
* valor nuevo;
* resultado de la corrección;
* motivo de la modificación.

Además, las auditorías pueden conservarse históricamente para permitir comparaciones posteriores.

Esto permite plantear un flujo de trabajo reproducible:

```text
Catálogo
   ↓
Auditoría inicial
   ↓
Detección de problemas
   ↓
Correcciones
   ↓
Nueva auditoría
   ↓
Comparación de resultados
```

---

## 6. ¿Qué demuestra este ejemplo?

Este caso demuestra una parte del enfoque de `biblioteca_analytics`:

* análisis automatizado de datos bibliográficos;
* validación de campos MARC21;
* identificación de inconsistencias;
* comparación con fuentes bibliográficas externas;
* aplicación de correcciones;
* trazabilidad de los cambios;
* medición de la evolución de la calidad del catálogo.

El objetivo no es únicamente detectar errores, sino poder **medir y documentar el proceso de mejora de los datos**.

---

## Estado del proyecto

🚧 **En desarrollo**

Las próximas etapas contemplan ampliar las reglas de validación, mejorar la detección de inconsistencias entre autores y materias, incorporar más controles bibliográficos y desarrollar indicadores y visualizaciones de calidad.
