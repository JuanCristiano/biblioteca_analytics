import json
import csv
from pathlib import Path


CARPETA_RAW = Path("data/raw")

RUTA_CATALOGO = CARPETA_RAW / "catalogo_marc_prueba_200.json"
RUTA_AUTORES = CARPETA_RAW / "fuente_autores_prueba_200.csv"


AUTORES = [
    "Borges, Jorge Luis",
    "Cortázar, Julio",
    "García Márquez, Gabriel",
    "Sábato, Ernesto",
    "Allende, Isabel",
    "Saramago, José",
    "Eco, Umberto",
    "Freire, Paulo",
    "Bauman, Zygmunt",
    "Bourdieu, Pierre",
    "Foucault, Michel",
    "Piaget, Jean",
    "Vygotsky, Lev S.",
    "Castells, Manuel",
    "Drucker, Peter F.",
    "Kotler, Philip",
    "Pressman, Roger S.",
    "Silberschatz, Abraham",
    "Tanenbaum, Andrew S.",
    "Russell, Stuart",
]


AREAS = [
    "Bibliotecología",
    "Educación",
    "Historia",
    "Sociología",
    "Psicología",
    "Derecho",
    "Economía",
    "Administración",
    "Informática",
    "Comunicación",
    "Filosofía",
    "Letras",
    "Ciencia Política",
    "Ciencias Ambientales",
    "Investigación",
]


EDITORIALES = [
    "Siglo XXI",
    "Paidós",
    "Ariel",
    "Alianza",
    "Fondo de Cultura Económica",
    "Eudeba",
    "McGraw-Hill",
    "Pearson",
    "Alfaomega",
    "Trea",
]


TITULOS = [
    "Introducción a la bibliotecología",
    "Gestión de bibliotecas universitarias",
    "Organización del conocimiento",
    "Metadatos para bibliotecas digitales",
    "Alfabetización informacional",
    "Metodología de la investigación",
    "La sociedad de la información",
    "Educación y tecnología",
    "Introducción a la psicología",
    "Historia social de América Latina",
    "Derecho y sociedad",
    "Economía para no economistas",
    "Administración estratégica",
    "Fundamentos de programación",
    "Bases de datos",
    "Comunicación institucional",
    "Introducción a la filosofía",
    "Literatura latinoamericana",
    "Ciencia política contemporánea",
    "Gestión ambiental",
]


SUBTITULOS = [
    "Fundamentos, conceptos y aplicaciones",
    "Teoría y práctica",
    "Perspectivas para la educación superior",
    "Principios y herramientas",
    "Problemas y debates contemporáneos",
    "Estrategias para estudiantes universitarios",
    "Conceptos fundamentales",
    "Métodos, técnicas y experiencias",
    "Una introducción crítica",
    "Enfoques y nuevas perspectivas",
]

def crear_isbn13(prefijo):
    suma = 0

    for posicion, digito in enumerate(prefijo):
        if posicion % 2 == 0:
            suma += int(digito)
        else:
            suma += int(digito) * 3

    digito_control = (10 - (suma % 10)) % 10

    return prefijo + str(digito_control)


def crear_registro(numero):
    identificador = f"{numero:06d}"

    autor = AUTORES[(numero - 1) % len(AUTORES)]
    titulo = TITULOS[(numero - 1) % len(TITULOS)]
    subtitulo = SUBTITULOS[(numero - 1) % len(SUBTITULOS)]
    area = AREAS[(numero - 1) % len(AREAS)]
    editorial = EDITORIALES[(numero - 1) % len(EDITORIALES)]

    anio = str(2010 + (numero % 16))

    prefijo_isbn = f"978950{numero:06d}"
    isbn = crear_isbn13(prefijo_isbn)

    registro = {
        "001": identificador,

        "020": [
            {
                "subcampos": {
                    "a": isbn
                }
            }
        ],

        "041": [
            {
                "subcampos": {
                    "a": "spa"
                }
            }
        ],

        "082": [
            {
                "subcampos": {
                    "a": str(100 + (numero % 800))
                }
            }
        ],

        "100": [
            {
                "subcampos": {
                    "a": autor
                }
            }
        ],

        "245": [
            {
                "subcampos": {
                    "a": titulo,
                    "b": subtitulo,
                    "c": autor
                }
            }
        ],

        "250": [
            {
                "subcampos": {
                    "a": "1a ed."
                }
            }
        ],

        "264": [
            {
                "subcampos": {
                    "b": editorial,
                    "c": anio
                }
            }
        ],

        "300": [
            {
                "subcampos": {
                    "a": f"{100 + numero} p.",
                    "b": "il.",
                    "c": "23 cm"
                }
            }
        ],

        "500": [
            {
                "subcampos": {
                    "a": "Incluye referencias y material complementario."
                }
            }
        ],

        "504": [
            {
                "subcampos": {
                    "a": "Incluye referencias bibliográficas."
                }
            }
        ],

        "520": [
            {
                "subcampos": {
                    "a": (
                        f"Obra relacionada con {area.lower()}, "
                        "destinada a estudiantes universitarios."
                    )
                }
            }
        ],

        "650": [
            {
                "subcampos": {
                    "a": area,
                    "x": "Enseñanza universitaria"
                }
            }
        ],

        "655": [
            {
                "subcampos": {
                    "a": "Material universitario"
                }
            }
        ],

        "700": [
            {
                "subcampos": {
                    "a": AUTORES[numero % len(AUTORES)]
                }
            }
        ],

        "852": [
            {
                "subcampos": {
                    "a": "Biblioteca Central",
                    "b": f"Sala {1 + (numero % 5)}",
                    "c": f"Estante {1 + (numero % 20)}"
                }
            }
        ],

        "856": [
            {
                "subcampos": {
                    "u": (
                        "https://biblioteca.example.edu/"
                        f"record/{identificador}"
                    ),
                    "y": "Acceso al registro"
                }
            }
        ],

        "952": [
            {
                "subcampos": {
                    "p": f"BC{numero:08d}"
                }
            }
        ],

        "_idioma": "spa",
        "_tipo_material": "Texto impreso"
    }

    return registro

def aplicar_anomalias(registro, numero):

    if numero in [8, 31, 72, 119]:
        registro.pop("245")

    if numero in [12, 44, 91, 133]:
        registro.pop("020")

    if numero in [17, 63, 104]:
        registro["020"][0]["subcampos"]["a"] = (
            crear_isbn13("978950000001")
        )

    if numero in [23, 77, 128]:
        registro.pop("100")

    if numero in [29, 58, 96]:
        autor = registro["100"][0]["subcampos"]["a"]

        autor = (
            autor
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
        )

        registro["100"][0]["subcampos"]["a"] = autor

    if numero in [52, 118]:
        autor_actual = registro["100"][0]["subcampos"]["a"]

        if autor_actual == "Borges, Jorge Luis":
            nuevo_autor = "Cortázar, Julio"
        else:
            nuevo_autor = "Borges, Jorge Luis"

        registro["100"][0]["subcampos"]["a"] = nuevo_autor

    if numero in [36, 88]:
        registro["264"][0]["subcampos"].pop("c")

    if numero in [48, 112]:
        registro["300"][0]["subcampos"].pop("a")

    if numero in [55, 101]:
        registro["650"] = [
            {
                "subcampos": {
                    "a": registro["650"][0]["subcampos"]["a"]
                }
            }
        ]

    if numero in [67, 124]:
        registro["856"][0]["subcampos"]["u"] = (
            "https://biblioteca.example.edu/record/"
        )

    if numero == 39:
        registro["245"][0]["subcampos"]["b"] = ""

    if numero == 83:
        registro["700"] = []

    if numero == 94:
        registro["856"] = []

    if numero == 109:
        registro["500"][0]["subcampos"]["a"] = (
            "Nota incompleta."
        )

def crear_fuente_autores(numero):
    autor = AUTORES[(numero - 1) % len(AUTORES)]

    if numero in [52, 118]:
        autor = AUTORES[(numero + 7) % len(AUTORES)]

    return autor


def guardar_catalogo(registros):
    CARPETA_RAW.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        RUTA_CATALOGO,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            registros,
            archivo,
            ensure_ascii=False,
            indent=2
        )


def guardar_fuente_autores(fuente):
    with open(
        RUTA_AUTORES,
        "w",
        encoding="utf-8",
        newline=""
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=["001", "autor"]
        )

        escritor.writeheader()
        escritor.writerows(fuente)


def main():
    registros = []
    fuente = []

    for numero in range(1, 201):
        registro = crear_registro(numero)

        aplicar_anomalias(
            registro,
            numero
        )

        registros.append(registro)

        fuente.append(
            {
                "001": f"{numero:06d}",
                "autor": crear_fuente_autores(numero)
            }
        )

    guardar_catalogo(registros)
    guardar_fuente_autores(fuente)

    print("=" * 50)
    print("CATÁLOGO DE PRUEBA GENERADO")
    print("=" * 50)
    print()
    print(f"Registros generados: {len(registros)}")
    print()
    print("Archivos creados:")
    print(f"- {RUTA_CATALOGO}")
    print(f"- {RUTA_AUTORES}")
    print()
    print("Generación finalizada correctamente.")


if __name__ == "__main__":
    main()        