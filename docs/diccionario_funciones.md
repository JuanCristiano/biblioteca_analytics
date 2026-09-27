# Diccionario de funciones bibliográficas

## Biblioteca Analytics

## 1. Objetivo

Este documento define las principales funciones bibliográficas que Biblioteca Analytics deberá reconocer al analizar un catálogo.

La herramienta no trabajará únicamente con números de campos MARC21. Intentará identificar qué función cumple cada dato dentro del registro bibliográfico.

Esto permite trabajar con bibliotecas que utilizan diferentes campos, configuraciones locales o prácticas de catalogación.

---

# 2. Principio general

Una misma función bibliográfica puede estar representada por diferentes campos MARC21.

Por ejemplo, la información relacionada con materias puede encontrarse en diferentes campos del bloque 6XX.

Por lo tanto:

```text
FUNCIÓN BIBLIOGRÁFICA
        ↓
uno o varios campos MARC21
        ↓
reglas de calidad
```

La herramienta no deberá asumir que la ausencia de un campo específico significa necesariamente que falta determinada información.

---

# 3. Identificación del registro

### Función

Identificar de manera única un registro bibliográfico.

### Campos principales

* 001 — Número de control
* 003 — Identificador de la agencia
* 005 — Fecha/hora de la última modificación
* 008 — Elementos de longitud fija

### Objetivo de auditoría

Detectar:

* registros sin identificador;
* identificadores duplicados;
* formatos inconsistentes;
* posibles conflictos entre identificadores.

### Nivel inicial

ERROR cuando exista duplicación de un identificador que debería ser único.

ADVERTENCIA cuando el identificador esté ausente o presente una estructura inesperada.

---

# 4. Identificación normalizada del recurso

## 4.1 ISBN

### Función

Identificar una edición o manifestación mediante un número normalizado.

### Campo

* 020

### Información relevante

* ISBN válido;
* ISBN inválido;
* ISBN-10;
* ISBN-13;
* ISBN cancelado o no válido;
* información calificadora.

### Auditoría

El sistema deberá poder detectar:

* ISBN inválidos;
* ISBN duplicados;
* formatos diferentes del mismo ISBN;
* ISBN faltantes;
* posibles conflictos entre ISBN y título/edición.

---

# 5. Autoría

## 5.1 Autor personal principal

### Función

Representar el principal punto de acceso correspondiente a una persona.

### Campo principal

* 100

### Información relacionada

* nombre;
* fechas;
* títulos;
* términos de relación;
* identificadores de autoridad.

### Auditoría

Detectar:

* nombres vacíos;
* posibles variantes;
* formatos inconsistentes;
* posibles duplicaciones;
* diferencias en la forma del nombre.

---

## 5.2 Entidad corporativa principal

### Campo

* 110

### Función

Representar una institución, organización u otra entidad corporativa como punto de acceso principal.

---

## 5.3 Reunión o congreso principal

### Campo

* 111

### Función

Representar una reunión, congreso, conferencia u otro evento similar como punto de acceso principal.

---

## 5.4 Autores y colaboradores secundarios

### Campos

* 700 — Nombre personal
* 710 — Entidad corporativa
* 711 — Reunión

### Función

Representar personas, instituciones o reuniones relacionadas con el recurso que no constituyen el punto de acceso principal.

---

# 6. Título

## 6.1 Título principal

### Campo

* 245

### Función

Representar el título principal del recurso y la información relacionada.

### Subcampos relevantes

* $a — Título
* $b — Resto del título
* $c — Mención de responsabilidad
* $n — Número de parte o sección
* $p — Nombre de parte o sección

### Auditoría

Detectar:

* título ausente;
* título vacío;
* posibles duplicaciones;
* inconsistencias;
* problemas evidentes de estructura.

---

## 6.2 Títulos relacionados o variantes

### Campos

* 246 — Forma variante del título
* 740 — Punto de acceso secundario de título

### Función

Representar formas alternativas, variantes o títulos relacionados.

---

## 6.3 Título uniforme

### Campos

* 130
* 240
* 730

### Función

Representar títulos uniformes utilizados como puntos de acceso.

---

# 7. Edición

### Campo principal

* 250

### Función

Registrar información relacionada con la edición del recurso.

### Auditoría

Detectar:

* valores vacíos;
* formatos inconsistentes;
* información aparentemente duplicada;
* posibles diferencias entre registros que podrían corresponder a distintas ediciones.

---

# 8. Publicación, producción y distribución

### Campos principales

* 260
* 264

### Función

Representar información relacionada con lugar, editor/productor/distribuidor y fecha.

### Información relevante

* lugar;
* nombre de la entidad;
* fecha;
* función de la entidad.

### Auditoría

Detectar:

* fechas ausentes;
* fechas imposibles;
* estructuras inconsistentes;
* diferencias relevantes entre registros;
* utilización de 260 y 264.

La presencia de 260 no deberá considerarse automáticamente un error.

---

# 9. Descripción física

### Campo

* 300

### Función

Describir las características físicas del recurso.

### Información relevante

* extensión;
* otros detalles físicos;
* dimensiones;
* material acompañante.

### Auditoría

Detectar:

* ausencia de información;
* valores anómalos;
* formatos inconsistentes;
* posibles duplicaciones.

---

# 10. Serie

### Campos

* 490
* 800
* 810
* 811
* 830

### Función

Representar información relacionada con series y sus puntos de acceso.

### Auditoría

Detectar:

* series incompletas;
* inconsistencias;
* diferencias entre la mención de serie y su punto de acceso;
* posibles duplicaciones.

---

# 11. Notas

El bloque 5XX contiene diferentes tipos de información complementaria.

## Principales funciones de interés

### 500 — Nota general

Información adicional sobre el recurso.

### 504 — Nota de bibliografía

Indica la existencia de bibliografía, referencias u otra información relacionada.

### 505 — Nota de contenido

Describe el contenido del recurso.

### 520 — Resumen

Contiene información resumida sobre el contenido.

### 546 — Nota de idioma

Indica información relacionada con el idioma.

### Principio

La herramienta deberá reconocer que cada campo 5XX tiene una función específica.

No deberá considerar todas las notas como equivalentes.

---

# 12. Materias y acceso temático

Esta será una de las áreas principales de Biblioteca Analytics.

## 12.1 Nombre personal como materia

### Campo

* 600

---

## 12.2 Entidad corporativa como materia

### Campo

* 610

---

## 12.3 Reunión como materia

### Campo

* 611

---

## 12.4 Título como materia

### Campo

* 630

---

## 12.5 Acontecimiento como materia

### Campo

* 647

---

## 12.6 Término cronológico

### Campo

* 648

---

## 12.7 Término temático

### Campo

* 650

---

## 12.8 Nombre geográfico

### Campo

* 651

---

## 12.9 Término temático no controlado

### Campo

* 653

---

## 12.10 Término temático facetado

### Campo

* 654

---

## 12.11 Género o forma

### Campo

* 655

---

## 12.12 Ocupación

### Campo

* 656

---

## 12.13 Función

### Campo

* 657

---

## 12.14 Objetivo curricular

### Campo

* 658

---

## 12.15 Lugar jerárquico

### Campo

* 662

---

# 13. Principio para la auditoría de materias

La herramienta no deberá utilizar una regla simplista como:

```text
"Si no existe 650 → falta materia"
```

En su lugar deberá analizar la totalidad de los campos de acceso temático configurados para la biblioteca.

Ejemplo:

```text
650 → materia temática
651 → materia geográfica
655 → género/forma
690 → materia local
```

Un registro que no tenga 650 pero sí tenga 651 y 655 no deberá ser considerado automáticamente como un registro sin materias.

---

# 14. Vocabularios controlados y autoridades

La calidad de una materia no depende solamente de que el campo exista.

Cuando sea posible, la herramienta podrá analizar:

* presencia de identificadores de autoridad;
* fuente del vocabulario;
* términos controlados;
* variantes;
* términos aparentemente duplicados;
* diferencias ortográficas;
* utilización de vocabularios diferentes.

Los subcampos de identificación de fuente y autoridad deberán analizarse según el campo correspondiente.

---

# 15. Campos locales

Los campos locales requieren un tratamiento especial.

Por ejemplo:

```text
690$a Literatura argentina
```

No deberá ser considerado automáticamente incorrecto.

Una biblioteca puede haber definido 690 para una función determinada.

Por eso Biblioteca Analytics deberá permitir configurar equivalencias.

Ejemplo:

```yaml
campos:
  materia:
    - 650
    - 653
    - 690

  materia_geografica:
    - 651

  genero:
    - 655
```

La configuración será específica de cada biblioteca.

---

# 16. Ejemplares

Los datos bibliográficos y los datos de ejemplares deberán diferenciarse.

La información del ejemplar puede encontrarse en campos locales o estructuras específicas del sistema de gestión utilizado.

Por ejemplo, en determinados entornos Koha se utiliza el campo 952 para información relacionada con ejemplares.

### Principio

Biblioteca Analytics deberá distinguir:

```text
REGISTRO BIBLIOGRÁFICO
        +
EJEMPLARES
```

y no asumir que toda la información de circulación, ubicación o inventario forma parte del registro bibliográfico.

---

# 17. Funciones futuras

El diccionario podrá ampliarse para incluir:

* idioma;
* audiencia;
* tipo de contenido;
* tipo de medio;
* tipo de soporte;
* clasificación;
* signatura topográfica;
* colección;
* procedencia;
* derechos;
* acceso electrónico;
* identificadores externos;
* autoridades;
* datos de ejemplares;
* información administrativa.

---

# 18. Principio de diseño

Biblioteca Analytics deberá trabajar con la siguiente lógica:

```text
CAMPO MARC21
      ↓
FUNCIÓN BIBLIOGRÁFICA
      ↓
REGLA DE CALIDAD
      ↓
RESULTADO
```

Ejemplo:

```text
650
 ↓
Materia temática
 ↓
Analizar término, indicadores, subcampos,
fuente de vocabulario y autoridad
 ↓
OK / ADVERTENCIA / ERROR
```

---

# 19. Principio profesional

La herramienta no deberá transformar automáticamente una anomalía en una corrección bibliográfica.

Su función será:

1. detectar;
2. clasificar;
3. explicar;
4. proporcionar evidencia;
5. sugerir una posible revisión.

La decisión final deberá permanecer bajo control del profesional bibliotecario.

---

# 20. Evolución

Este diccionario será ampliado a medida que Biblioteca Analytics incorpore nuevas reglas, tipos de recursos, campos MARC21, sistemas de gestión y necesidades de migración.
