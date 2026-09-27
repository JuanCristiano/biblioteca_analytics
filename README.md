\# Biblioteca Analytics



\*\*Proyecto de análisis, auditoría y control de calidad de datos bibliográficos mediante Python y metadatos MARC21.\*\*



Biblioteca Analytics explora cómo las herramientas de programación y análisis de datos pueden aplicarse a problemas reales de gestión bibliotecaria, especialmente en procesos de \*\*migración, normalización, limpieza y control de calidad de catálogos\*\*.



El proyecto combina experiencia en \*\*bibliotecología y gestión de información\*\* con herramientas de \*\*Python, procesamiento de datos, validación y automatización\*\*.



\---



\##  Problema a resolver



Los catálogos bibliográficos pueden acumular errores e inconsistencias a lo largo del tiempo, especialmente cuando los datos provienen de diferentes sistemas, formatos, procesos de migración o falta de personal profesional.



Algunos ejemplos:



\* títulos incompletos;

\* autores ausentes o inconsistentes;

\* ISBN inválidos o duplicados;

\* fechas de publicación faltantes;

\* información editorial incompleta;

\* descripciones físicas inconsistentes;

\* enlaces incorrectos;

\* diferentes formas de representar un mismo autor;

\* registros duplicados;

\* archivos CSV con estructuras y columnas diferentes.



Estos problemas pueden afectar la recuperación de información y aumentar el trabajo necesario para mantener un catálogo de calidad.



\---



\## Objetivo



Biblioteca Analytics busca desarrollar un flujo de trabajo que permita:



1\. cargar datos bibliográficos provenientes de diferentes fuentes;

2\. analizar su estructura y contenido;

3\. normalizar los datos;

4\. aplicar reglas de control de calidad;

5\. detectar inconsistencias y duplicados;

6\. comparar determinados datos con fuentes bibliográficas externas;

7\. evaluar la confianza de determinadas coincidencias o sugerencias;

8\. proponer y aplicar correcciones;

9\. registrar las modificaciones realizadas;

10\. generar informes de calidad;

11\. comparar diferentes auditorías para medir la evolución del catálogo.



\---



\##  Flujo general del sistema



```text

\&#x20;                CATÁLOGO

\&#x20;                   │

\&#x20;                   ▼

\&#x20;         Carga / Conversión

\&#x20;                   │

\&#x20;                   ▼

\&#x20;            Normalización

\&#x20;                   │

\&#x20;                   ▼

\&#x20;         Validación de datos

\&#x20;                   │

\&#x20;                   ▼

\&#x20;              Auditoría

\&#x20;                   │

\&#x20;         ┌─────────┴─────────┐

\&#x20;         ▼                   ▼

\&#x20;  Reglas MARC21       Fuentes externas

\&#x20;         │                   │

\&#x20;         └─────────┬─────────┘

\&#x20;                   ▼

\&#x20;         Evaluación / Comparación

\&#x20;                   │

\&#x20;                   ▼

\&#x20;            Correcciones

\&#x20;                   │

\&#x20;                   ▼

\&#x20;          Historial de cambios

\&#x20;                   │

\&#x20;                   ▼

\&#x20;          Informe de calidad

\&#x20;                   │

\&#x20;                   ▼

\&#x20;       Comparación de auditorías

```



\---



\## Funcionalidades desarrolladas



\###  Auditoría de calidad



El proyecto cuenta con diferentes reglas para detectar problemas en registros bibliográficos.



Actualmente se incluyen validaciones relacionadas con:



\* título;

\* subtítulo;

\* autor principal;

\* ISBN;

\* año de publicación;

\* información de publicación;

\* descripción física;

\* enlaces;

\* extensiones;

\* registros duplicados.



Las reglas se encuentran organizadas en:



```text

modulos/

└── calidad\\\_datos/

\&#x20;   └── reglas/

```



\---



\###  Validación de identificadores



El proyecto incorpora funciones para normalizar y validar identificadores bibliográficos.



Se contemplan:



\* ISBN-10;

\* ISBN-13;

\* ISSN.



Las validaciones incluyen, según el tipo de identificador, comprobaciones de formato y dígitos de control.



También se pueden detectar identificadores duplicados dentro del catálogo.



\---



\###  Normalización y comparación de autores



Una parte del proyecto está dedicada a resolver uno de los problemas habituales de los datos bibliográficos: distintas representaciones de una misma persona.



Por ejemplo:



```text

Roald Dahl

Dahl, Roald

```



o:



```text

García Márquez, Gabriel

Gabriel García Márquez

```



La normalización contempla diferencias como:



\* mayúsculas y minúsculas;

\* acentos;

\* orden del nombre;

\* formato apellido/nombre;

\* múltiples autores.



\---



\###  Comparación de información bibliográfica



Biblioteca Analytics puede consultar fuentes bibliográficas externas para contrastar información del catálogo.



Actualmente se utiliza \*\*Open Library\*\* como fuente de referencia para determinados registros.



Se pueden comparar datos como:



\* título;

\* autor;

\* identificadores.



Las comparaciones permiten distinguir entre diferentes niveles de coincidencia y situaciones en las que no existe información suficiente para realizar una comparación.



\---



\###  Evaluación de confianza



El proyecto incorpora un componente destinado a evaluar la confianza de determinadas coincidencias o sugerencias antes de utilizarlas para una corrección.



La idea es diferenciar entre:



```text

Coincidencia confiable

\&#x20;       ↓

Coincidencia posible

\&#x20;       ↓

Revisión manual

```



Esto busca evitar que una coincidencia aproximada termine convirtiéndose automáticamente en un dato bibliográfico incorrecto.



\---



\###  Correcciones y trazabilidad



El proyecto incorpora un mecanismo para aplicar correcciones y registrar los cambios realizados.



Por ejemplo:



```text

Registro: 000036



Campo: 264$c



Valor anterior:

Valor nuevo: 2020

```



El historial permite conservar información como:



\* identificador del registro;

\* campo modificado;

\* subcampo;

\* valor anterior;

\* valor nuevo;

\* resultado de la operación.



El objetivo es que la limpieza de datos sea \*\*trazable y auditable\*\*, en lugar de modificar el catálogo sin conservar evidencia del cambio.



\---



\##  Historial y comparación de auditorías



Una característica importante del proyecto es la posibilidad de conservar diferentes auditorías y compararlas posteriormente.



Esto permite analizar la evolución de la calidad del catálogo.



Por ejemplo:



```text

Auditoría 1

\&#x20;   ↓

Proceso de limpieza

\&#x20;   ↓

Auditoría 2

\&#x20;   ↓

Comparación

\&#x20;   ↓

Medición de cambios

```



De esta manera, el sistema no se limita a detectar problemas: también busca permitir evaluar el resultado del trabajo de limpieza bibliográfica.



\---



\##  Estructura del proyecto



```text

biblioteca\\\_analytics/

│

├── data/

│   ├── generator/

│   └── raw/

│

├── docs/

│   ├── diccionario\\\_funciones.md

│   └── modelo\\\_marc21.md

│

├── modulos/

│   ├── calidad\\\_datos/

│   │   └── reglas/

│   │

│   └── cargadores/

│

├── tests/

│

├── auditar\\\_catalogo.py

├── auditoria.py

├── comparador\\\_bibliografico.py

├── comparar\\\_autores.py

├── comparar\\\_titulos.py

├── fuentes\\\_bibliograficas.py

├── identificadores.py

├── normalizacion.py

└── similitud\\\_texto.py

```



\### `modulos/calidad\\\_datos`



Contiene componentes relacionados con:



\* auditoría;

\* reglas de validación;

\* informes;

\* resúmenes;

\* exportación de resultados;

\* comparación entre auditorías;

\* aplicación de correcciones;

\* historial de cambios.



\### `modulos/cargadores`



Contiene herramientas para trabajar con diferentes fuentes y estructuras de datos:



\* CSV;

\* JSON;

\* fuentes de autores;

\* análisis de archivos;

\* mapeo de columnas;

\* normalización;

\* conversión a MARC;

\* evaluación de confianza;

\* validación de contenido.



\### `tests`



Contiene pruebas automatizadas para diferentes componentes del proyecto.



\---



\##  Datos de prueba



El proyecto utiliza catálogos sintéticos para probar diferentes escenarios de calidad.



Los datos permiten trabajar con casos como:



\* registros correctos;

\* campos incompletos;

\* identificadores inválidos;

\* identificadores duplicados;

\* autores con diferentes formatos;

\* múltiples autores;

\* diferencias entre fuentes;

\* posibles correcciones.



Los datos de prueba se encuentran en:



```text

data/raw/

```



\---



\##  Tecnologías



\### Lenguaje



\* Python



\### Datos y metadatos



\* MARC21

\* CSV

\* JSON



\### Procesamiento



\* Normalización de datos

\* Validación

\* Comparación de texto

\* Detección de duplicados

\* Auditoría de calidad

\* Evaluación de coincidencias

\* Corrección de datos



\### Fuentes bibliográficas



\* Open Library



\### Testing y control de versiones



\* Python testing

\* Git

\* GitHub



\---



\## Contexto bibliotecológico



El proyecto surge de la experiencia profesional en:



\* gestión de bibliotecas;

\* catalogación;

\* gestión de información;

\* repositorios digitales;

\* Koha;

\* DSpace;

\* normalización de datos;

\* metadatos bibliográficos;

\* administración de información.



La propuesta es explorar cómo Python y las técnicas de análisis de datos pueden complementar el trabajo bibliotecario, particularmente en procesos de \*\*migración, limpieza y control de calidad de catálogos\*\*.



\---



\##  Próximos pasos



El proyecto continúa en desarrollo.



Entre las próximas etapas se encuentran:



\* ampliar las reglas de validación bibliográfica;

\* mejorar la detección de inconsistencias en autores y materias;

\* ampliar las correcciones asistidas;

\* mejorar el cálculo de confianza;

\* incorporar más fuentes bibliográficas;

\* ampliar la cobertura de pruebas automatizadas;

\* desarrollar indicadores de calidad;

\* incorporar visualizaciones;

\* desarrollar un dashboard con Power BI;

\* explorar la integración con SQL;

\* mejorar la documentación y reproducibilidad del proyecto.



\---



\##  Autoria



\*\*Juan Gabriel Cristiano\*\*



\*\*Bibliotecario Profesional\*\* especializado en gestión de información y datos.



Experiencia profesional en bibliotecas, repositorios digitales, gestión de información y coordinación de equipos.



Actualmente desarrollando proyectos de \*\*Data Analytics, Python, SQL y calidad de datos aplicados al ámbito bibliotecario\*\*.



\---



\##  Estado del proyecto



\*\*En desarrollo\*\*



Biblioteca Analytics es un proyecto de portfolio y desarrollo continuo. Las funcionalidades se incorporan progresivamente a medida que los diferentes componentes son desarrollados y probados.

