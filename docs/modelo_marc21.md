# Modelo MARC21 — Biblioteca Analytics

## 1. Propósito

Este documento define el modelo de referencia MARC21 utilizado por Biblioteca Analytics para interpretar, analizar y auditar registros bibliográficos.

El objetivo no es reemplazar las normas de catalogación ni determinar automáticamente si un registro está correctamente catalogado desde el punto de vista profesional.

Biblioteca Analytics utilizará MARC21 como estructura de referencia para:

* identificar campos y subcampos;
* reconocer funciones bibliográficas;
* detectar problemas de estructura;
* detectar datos faltantes;
* detectar inconsistencias;
* identificar posibles duplicados;
* analizar campos locales;
* preparar información para procesos de migración;
* generar alertas para revisión profesional.

La herramienta deberá ser capaz de trabajar con catálogos procedentes de diferentes sistemas y prácticas de catalogación.

---

# 2. Principio fundamental

Un mismo tipo de información bibliográfica puede estar representado de diferentes maneras según el catálogo, el sistema utilizado y las decisiones de la biblioteca.

Por lo tanto, Biblioteca Analytics no deberá asumir que una única etiqueta MARC representa universalmente una determinada función.

Ejemplo:

```text
Materia temática:
650
653
654
690-699 (campos locales, según configuración)
```

La herramienta deberá diferenciar entre:

1. campos MARC21 estándar;
2. campos locales;
3. configuración particular de cada biblioteca.

---

# 3. Estructura general MARC21

Biblioteca Analytics reconocerá las principales familias de campos MARC21 bibliográficos:

| Bloque  | Descripción                                    |
| ------- | ---------------------------------------------- |
| 00X     | Campos de control                              |
| 01X-09X | Números, códigos y otros campos de información |
| 1XX     | Puntos de acceso principales                   |
| 20X-24X | Títulos                                        |
| 25X-28X | Edición y publicación/distribución             |
| 3XX     | Descripción física y características           |
| 4XX     | Menciones de serie                             |
| 5XX     | Notas                                          |
| 6XX     | Accesos temáticos                              |
| 7XX     | Puntos de acceso secundarios                   |
| 8XX     | Puntos de acceso de serie                      |
| 9XX     | Campos locales                                 |

---

# 4. Diccionario de funciones bibliográficas

El sistema trabajará principalmente con funciones bibliográficas y no solamente con números de campo.

Una función puede estar representada por uno o varios campos MARC.

## 4.1 Identificación del registro

### Función

Identificador/control del registro bibliográfico.

### Campos principales

* 001 — Número de control
* 003 — Identificador de la agencia
* 005 — Identificador de la versión
* 008 — Elementos de longitud fija

### Reglas iniciales

* 001 debería existir.
* El valor de 001 debería ser identificable de manera única dentro del catálogo.
* 001 no debería repetirse entre registros.
* 005 debe presentar un formato válido cuando esté presente.
* 008 debe cumplir con la estructura correspondiente al tipo de registro.

---

# 5. Identificación normalizada

## 5.1 ISBN

### Función

Número internacional normalizado del libro.

### Campo principal

* 020

### Subcampos relevantes

* $a — ISBN
* $q — Información calificadora
* $z — ISBN cancelado/no válido

### Reglas iniciales

El sistema deberá poder:

* detectar ISBN-10;
* detectar ISBN-13;
* validar dígitos de control;
* detectar formatos incorrectos;
* identificar ISBN faltantes;
* identificar ISBN duplicados;
* distinguir entre ISBN válido e ISBN cancelado/no válido;
* conservar información calificadora cuando exista.

---

# 6. Puntos de acceso principales

## 6.1 Autoridad personal principal

### Función

Punto de acceso principal correspondiente a una persona.

### Campo

* 100

### Subcampos relevantes

* $a — Nombre personal
* $b — Numeración
* $c — Títulos y otras palabras asociadas
* $d — Fechas asociadas
* $e — Término de relación
* $q — Forma más completa del nombre

### Auditoría

Se podrá analizar:

* ausencia del campo cuando corresponda;
* nombres vacíos;
* inconsistencias de formato;
* variantes;
* duplicaciones;
* presencia de identificadores de autoridad cuando corresponda.

---

## 6.2 Entidad corporativa principal

### Campo

* 110

---

## 6.3 Reunión o congreso principal

### Campo

* 111

---

# 7. Títulos

## 7.1 Título principal

### Campo

* 245

### Subcampos relevantes

* $a — Título
* $b — Resto del título
* $c — Mención de responsabilidad
* $n — Número de parte/sección
* $p — Nombre de parte/sección

### Auditoría

Se podrá analizar:

* existencia del título;
* título vacío;
* estructura del campo;
* presencia de información aparentemente duplicada;
* inconsistencias;
* caracteres o formatos anómalos.

---

## 7.2 Título uniforme

### Campo

* 130

## 7.3 Título uniforme secundario

### Campo

* 240

## 7.4 Variantes del título

### Campo

* 246

---

# 8. Edición

### Campo principal

* 250

### Función

Registrar información relativa a la edición.

### Auditoría

* presencia de información;
* formatos inconsistentes;
* duplicaciones;
* posibles anomalías.

---

# 9. Publicación, producción y distribución

### Campo principal

* 264

### Subcampos relevantes

* $a — Lugar
* $b — Nombre
* $c — Fecha

### Campo histórico/alternativo

* 260

### Principio

El sistema deberá reconocer tanto estructuras basadas en 260 como estructuras basadas en 264.

No deberá considerar automáticamente que la presencia de 260 constituye un error.

Deberá generar una alerta contextual cuando corresponda a una política de migración o al modelo de destino.

---

# 10. Descripción física

### Campo principal

* 300

### Subcampos relevantes

* $a — Extensión
* $b — Otros detalles físicos
* $c — Dimensiones
* $e — Material acompañante

### Auditoría

Se podrán detectar:

* ausencia;
* formatos inconsistentes;
* valores anómalos;
* duplicaciones;
* incompatibilidades evidentes.

---

# 11. Serie

### Campos principales

* 490 — Mención de serie
* 800 — Serie asociada a nombre personal
* 810 — Serie asociada a entidad corporativa
* 811 — Serie asociada a reunión
* 830 — Serie asociada a título uniforme

---

# 12. Notas

El bloque 5XX podrá contener diferentes tipos de notas.

### Campos iniciales de interés

* 500 — Nota general
* 504 — Nota de bibliografía
* 505 — Nota de contenido
* 520 — Resumen, etc.
* 546 — Nota de idioma

### Principio

La herramienta deberá identificar el tipo de nota según el campo utilizado.

No deberá tratar todos los campos 5XX como equivalentes.

---

# 13. Accesos temáticos

El bloque 6XX será tratado como una familia de funciones relacionadas con acceso temático.

## 13.1 Nombre personal como materia

* 600

## 13.2 Entidad corporativa como materia

* 610

## 13.3 Reunión como materia

* 611

## 13.4 Título como materia

* 630

## 13.5 Acontecimiento como materia

* 647

## 13.6 Término cronológico

* 648

## 13.7 Término temático

* 650

## 13.8 Nombre geográfico

* 651

## 13.9 Término temático no controlado

* 653

## 13.10 Término temático facetado

* 654

## 13.11 Género/forma

* 655

## 13.12 Ocupación

* 656

## 13.13 Función

* 657

## 13.14 Objetivo curricular

* 658

## 13.15 Lugar jerárquico

* 662

### Principio de auditoría

La ausencia de 650 no deberá interpretarse automáticamente como ausencia de materias.

El sistema deberá revisar otros campos 6XX y, cuando corresponda, campos locales configurados por la biblioteca.

---

# 14. Puntos de acceso secundarios

## Campos principales

* 700 — Nombre personal
* 710 — Entidad corporativa
* 711 — Reunión
* 730 — Título uniforme
* 740 — Título relacionado/no controlado

Estos campos podrán representar autores secundarios, colaboradores, entidades, títulos y otros puntos de acceso.

La interpretación deberá realizarse considerando indicadores y subcampos.

---

# 15. Puntos de acceso de serie

Campos principales:

* 800
* 810
* 811
* 830

La herramienta deberá distinguir los diferentes tipos de punto de acceso de serie.

---

# 16. Campos locales

Los campos 9XX y otros campos definidos localmente deberán tratarse de manera configurable.

Biblioteca Analytics no deberá considerar automáticamente un campo local como incorrecto.

Ejemplo:

```text
690$a Literatura argentina
```

Podrá representar información temática local dependiendo de la política de la biblioteca.

La herramienta deberá poder recibir una configuración que indique la función asignada por una determinada biblioteca.

Ejemplo conceptual:

```yaml
campos:
  materia:
    - 650
    - 653
    - 690

  materia_geografica:
    - 651

  autor_principal:
    - 100
```

---

# 17. Indicadores

El análisis MARC21 deberá contemplar los indicadores de cada campo cuando corresponda.

Los indicadores no deberán ser tratados como simples caracteres sin significado.

Una regla podrá evaluar:

* existencia;
* valores permitidos;
* combinación de indicadores;
* coherencia con los subcampos;
* estructura esperada del campo.

---

# 18. Subcampos

El análisis deberá contemplar la estructura interna de los campos mediante subcampos.

Ejemplo:

```text
650 #4 $a Literatura argentina $2 ...
```

La auditoría podrá evaluar:

* subcampos obligatorios;
* subcampos permitidos;
* subcampos repetibles;
* valores vacíos;
* combinaciones inconsistentes;
* presencia o ausencia de identificadores.

---

# 19. Repetibilidad

La herramienta deberá diferenciar entre:

* campos repetibles;
* campos no repetibles;
* subcampos repetibles;
* subcampos no repetibles.

La repetición de un campo no deberá considerarse automáticamente un error.

---

# 20. Regla fundamental del sistema

Biblioteca Analytics deberá distinguir entre:

### ERROR

Incumplimiento estructural o inconsistencia que requiere revisión.

### ADVERTENCIA

Situación potencialmente problemática que requiere análisis profesional.

### INFORMACIÓN

Dato relevante para el análisis pero que no constituye necesariamente un problema.

### CONFIGURACIÓN LOCAL

Comportamiento definido por la propia biblioteca.

---

# 21. Principio profesional

Biblioteca Analytics es una herramienta de auditoría y apoyo a la gestión de datos bibliográficos.

No reemplaza:

* al catalogador;
* las políticas de la biblioteca;
* las normas de catalogación;
* los catálogos de autoridad;
* la evaluación profesional;
* las decisiones de migración.

El sistema identifica problemas y proporciona evidencia para facilitar la revisión profesional.

---

# 22. Evolución del modelo

Este documento será ampliado progresivamente.

Las futuras versiones podrán incorporar:

* mayor cobertura de campos MARC21;
* validación avanzada de indicadores;
* validación de subcampos;
* autoridades;
* vocabularios controlados;
* RDA;
* AACR2;
* correspondencias entre MARC21 y modelos de destino;
* reglas específicas para Koha;
* reglas específicas para procesos de migración;
* perfiles de configuración por biblioteca.
