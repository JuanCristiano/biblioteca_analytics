from pathlib import Path

import pytest

from modulos.cargadores.cargar_csv import cargar_catalogo_csv

RUTA_CATALOGO_PRUEBA = (
    Path(__file__).resolve().parent.parent / "data" / "raw" / "catalogo_prueba.csv"
)


def crear_csv(tmp_path, texto, encoding="utf-8"):
    # Se escriben los bytes tal cual para que el salto de línea sea el mismo en cualquier sistema.
    ruta = tmp_path / "catalogo.csv"
    ruta.write_bytes(texto.encode(encoding))
    return ruta


# ---------- Lo básico ----------

def test_devuelve_un_diccionario_por_fila_con_los_encabezados_como_claves(tmp_path):
    ruta = crear_csv(
        tmp_path,
        "001,titulo,autor\n"
        "1,Rayuela,Julio Cortázar\n"
        "2,El Aleph,Jorge Luis Borges\n",
    )

    assert cargar_catalogo_csv(ruta) == [
        {"001": "1", "titulo": "Rayuela", "autor": "Julio Cortázar"},
        {"001": "2", "titulo": "El Aleph", "autor": "Jorge Luis Borges"},
    ]


def test_conserva_el_orden_de_las_filas(tmp_path):
    ruta = crear_csv(tmp_path, "001,titulo\n3,c\n1,a\n2,b\n")

    assert [r["001"] for r in cargar_catalogo_csv(ruta)] == ["3", "1", "2"]


def test_todos_los_valores_son_texto_y_conservan_los_ceros_iniciales(tmp_path):
    ruta = crear_csv(tmp_path, "001,isbn,anio\n000001,0306406152,1998\n")

    registro = cargar_catalogo_csv(ruta)[0]

    assert registro == {"001": "000001", "isbn": "0306406152", "anio": "1998"}


def test_conserva_tildes_y_enies(tmp_path):
    ruta = crear_csv(tmp_path, "titulo,autor\nCien años de soledad,Gabriel García Márquez\n")

    assert cargar_catalogo_csv(ruta)[0] == {
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
    }


def test_un_valor_vacio_es_texto_vacio_y_no_none(tmp_path):
    ruta = crear_csv(tmp_path, "001,titulo,autor\n8,,Roald Dahl\n")

    assert cargar_catalogo_csv(ruta)[0] == {"001": "8", "titulo": "", "autor": "Roald Dahl"}


# ---------- Formato del archivo ----------

def test_el_bom_no_se_pega_al_primer_encabezado(tmp_path):
    ruta = crear_csv(tmp_path, "001,titulo\n1,Rayuela\n", encoding="utf-8-sig")

    assert cargar_catalogo_csv(ruta) == [{"001": "1", "titulo": "Rayuela"}]


def test_un_campo_entre_comillas_puede_contener_comas(tmp_path):
    ruta = crear_csv(tmp_path, 'autor,titulo\n"Borges, Jorge Luis",El Aleph\n')

    assert cargar_catalogo_csv(ruta)[0] == {"autor": "Borges, Jorge Luis", "titulo": "El Aleph"}


def test_un_campo_entre_comillas_puede_contener_saltos_de_linea(tmp_path):
    ruta = crear_csv(tmp_path, 'titulo,autor\n"Primera línea\nsegunda línea",Cortázar\n')

    registros = cargar_catalogo_csv(ruta)

    assert len(registros) == 1
    assert registros[0]["titulo"] == "Primera línea\nsegunda línea"


def test_las_lineas_en_blanco_se_ignoran(tmp_path):
    ruta = crear_csv(tmp_path, "001,titulo\n1,a\n\n2,b\n\n")

    assert [r["001"] for r in cargar_catalogo_csv(ruta)] == ["1", "2"]


def test_un_archivo_con_solo_encabezados_devuelve_una_lista_vacia(tmp_path):
    assert cargar_catalogo_csv(crear_csv(tmp_path, "001,titulo,autor\n")) == []


def test_un_archivo_vacio_devuelve_una_lista_vacia(tmp_path):
    assert cargar_catalogo_csv(crear_csv(tmp_path, "")) == []


def test_acepta_la_ruta_como_texto(tmp_path):
    ruta = crear_csv(tmp_path, "001\n1\n")

    assert cargar_catalogo_csv(str(ruta)) == [{"001": "1"}]


# ---------- Catálogo de prueba real ----------
# Depende del archivo data/raw/catalogo_prueba.csv: es material de prueba fijo.
# Si lo cambiás a propósito, actualizá estos valores.

def test_carga_el_catalogo_de_prueba():
    catalogo = cargar_catalogo_csv(RUTA_CATALOGO_PRUEBA)

    assert len(catalogo) == 10
    assert list(catalogo[0]) == ["001", "titulo", "autor", "isbn", "editorial", "anio"]
    assert [r["001"] for r in catalogo] == [f"{n:06d}" for n in range(1, 11)]

    titulos = {r["001"]: r["titulo"] for r in catalogo}
    assert titulos["000001"] == "El Aleph"
    assert titulos["000004"] == "Cien años de soledad"
    assert titulos["000008"] == ""
    assert titulos["000009"] == "El Aleph"


# ---------- Limitaciones conocidas ----------
# Documentan lo que la función hace HOY. Si la mejorás y alguno falla,
# es una buena noticia: actualizá el test.

def test_limitacion_solo_entiende_la_coma_como_separador(tmp_path):
    # Es lo que produce Excel en español. No usa la detección de separador de analizar_csv.
    ruta = crear_csv(tmp_path, "001;titulo;autor\n1;Rayuela;Cortázar\n")

    assert cargar_catalogo_csv(ruta) == [
        {"001;titulo;autor": "1;Rayuela;Cortázar"}
    ]


def test_limitacion_un_archivo_guardado_como_ansi_no_se_puede_leer(tmp_path):
    ruta = crear_csv(tmp_path, "código,título\n1,Rayuela\n", encoding="cp1252")

    with pytest.raises(UnicodeDecodeError):
        cargar_catalogo_csv(ruta)


def test_limitacion_una_fila_con_menos_columnas_deja_none_en_las_que_faltan(tmp_path):
    ruta = crear_csv(tmp_path, "001,titulo,autor\n1,Rayuela\n")

    assert cargar_catalogo_csv(ruta) == [{"001": "1", "titulo": "Rayuela", "autor": None}]


def test_limitacion_una_fila_con_mas_columnas_guarda_el_sobrante_bajo_la_clave_none(tmp_path):
    ruta = crear_csv(tmp_path, "001,titulo\n1,Rayuela,sobra,otro\n")

    assert cargar_catalogo_csv(ruta) == [
        {"001": "1", "titulo": "Rayuela", None: ["sobra", "otro"]}
    ]


def test_limitacion_con_encabezados_repetidos_se_pierde_el_primer_valor(tmp_path):
    ruta = crear_csv(tmp_path, "autor,autor\nBorges,Bioy Casares\n")

    assert cargar_catalogo_csv(ruta) == [{"autor": "Bioy Casares"}]


def test_limitacion_no_limpia_espacios_ni_en_encabezados_ni_en_valores(tmp_path):
    ruta = crear_csv(tmp_path, " titulo ,autor\n Rayuela , Cortázar \n")

    assert cargar_catalogo_csv(ruta) == [
        {" titulo ": " Rayuela ", "autor": " Cortázar "}
    ]