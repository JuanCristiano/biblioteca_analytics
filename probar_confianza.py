from modulos.cargadores.evaluar_confianza import (
    evaluar_mapeo
)


mapeo_prueba = {

    # ==========================================
    # CASOS QUE YA CONOCEMOS
    # ==========================================

    "Título principal": "titulo",
    "Responsable": "autor",
    "ISBN-13": "isbn",


    # ==========================================
    # SINÓNIMOS
    # ==========================================

    "Nombre del libro": "titulo",
    "Autor principal": "autor",
    "Editor": "editorial",


    # ==========================================
    # MAYÚSCULAS / MINÚSCULAS
    # ==========================================

    "responsable": "autor",
    "RESPONSABLE": "autor",
    "Responsable": "autor",


    # ==========================================
    # POSIBLES ERRORES DE TIPEO
    # ==========================================

    "ResponsabIe": "autor",
    "Responsabl": "autor",
    "Responable": "autor",

    "Titlo": "titulo",
    "Titulu": "titulo",
    "Títul": "titulo",

    "ISN": "isbn",
    "ISSN": "isbn",


    # ==========================================
    # PALABRAS PARECIDAS PERO DIFERENTES
    # ==========================================

    "Autoridad": "autor",
    "Autorización": "autor",


    # ==========================================
    # VARIACIONES MÁS COMPLEJAS
    # ==========================================

    "Autor": "autor",
    "Autores": "autor",
    "Nombre del autor": "autor",
    "Apellido del autor": "autor",


    # ==========================================
    # MATERIAS / ASIGNATURAS
    # ==========================================

    "Materia": "materia",
    "Asignatura": "materia",
    "Materia bibliográfica": "materia",
    "Área temática": "materia",


    # ==========================================
    # CASO ABSURDO / INCORRECTO
    # ==========================================

    "Color de tapa": "titulo"

}


resultados = evaluar_mapeo(
    mapeo_prueba
)


print("EVALUACIÓN DE CONFIANZA")
print("=======================")
print()


for resultado in resultados:

    print(
        f"{resultado['columna_original']} "
        f"→ "
        f"{resultado['campo_estandar']}"
    )

    print(
        f"Confianza: "
        f"{resultado['confianza']}"
    )

    print(
        f"Motivo: "
        f"{resultado['motivo']}"
    )

    print()
