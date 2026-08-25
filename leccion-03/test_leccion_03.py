"""Tests de la Lección 03. NO los edites."""

import inspect

import pytest
from ejercicios_03 import (
    agrupar_por_inicial,
    fusionar_config,
    mas_larga,
    ordenar_catalogo,
    ordenar_desc,
    ordenar_por_edad,
    ordenar_por_largo,
    ranking,
    repetidos,
    separar_cabecera,
    top_palabras,
)

CATALOGO = [
    {"nombre": "teclado", "categoria": "accesorio", "precio": 50},
    {"nombre": "monitor", "categoria": "pantalla", "precio": 300},
    {"nombre": "mouse", "categoria": "accesorio", "precio": 20},
    {"nombre": "tablet", "categoria": "pantalla", "precio": 150},
]


# 1 -------------------------------------------------------------------------
def test_ordenar_por_largo():
    assert ordenar_por_largo(["python", "es", "genial"]) == ["es", "python", "genial"]
    assert ordenar_por_largo([]) == []


def test_ordenar_por_largo_es_estable():
    """Al empatar en largo, se conserva el orden original."""
    assert ordenar_por_largo(["bb", "aa", "c"]) == ["c", "bb", "aa"]


# 2 -------------------------------------------------------------------------
def test_ordenar_desc():
    assert ordenar_desc([3, 1, 2]) == [3, 2, 1]
    assert ordenar_desc([]) == []


def test_ordenar_desc_no_modifica_el_original():
    original = [3, 1, 2]
    ordenar_desc(original)
    assert original == [3, 1, 2], "usaste .sort() en vez de sorted()"


# 3 -------------------------------------------------------------------------
def test_mas_larga():
    assert mas_larga(["hola", "buenas", "chau"]) == "buenas"
    assert mas_larga(["unica"]) == "unica"


def test_mas_larga_empate_gana_la_primera():
    assert mas_larga(["abc", "xyz"]) == "abc"


def test_mas_larga_vacia():
    assert mas_larga([]) is None


# 4 -------------------------------------------------------------------------
def test_ordenar_por_edad():
    personas = [
        {"nombre": "Ana", "edad": 30},
        {"nombre": "Luis", "edad": 25},
        {"nombre": "Sofi", "edad": 41},
    ]
    assert [p["nombre"] for p in ordenar_por_edad(personas)] == ["Luis", "Ana", "Sofi"]
    assert ordenar_por_edad([]) == []


# 5 -------------------------------------------------------------------------
def test_ordenar_catalogo():
    resultado = [p["nombre"] for p in ordenar_catalogo(CATALOGO)]
    assert resultado == ["mouse", "teclado", "tablet", "monitor"]


def test_ordenar_catalogo_no_modifica_el_original():
    copia = [dict(p) for p in CATALOGO]
    ordenar_catalogo(CATALOGO)
    assert CATALOGO == copia


# 6 -------------------------------------------------------------------------
def test_ranking():
    assert ranking({"ana": 5, "luis": 8, "zoe": 5}) == ["luis", "ana", "zoe"]
    assert ranking({}) == []


def test_ranking_empate_alfabetico():
    """Todos empatados: queda el orden alfabético puro."""
    assert ranking({"zoe": 1, "ana": 1, "beto": 1}) == ["ana", "beto", "zoe"]


def test_ranking_no_invierte_el_alfabetico():
    """Si usaste reverse=True, este test te delata."""
    assert ranking({"b": 2, "a": 2, "c": 9}) == ["c", "a", "b"]


# 7 -------------------------------------------------------------------------
def test_top_palabras():
    assert top_palabras("el gato y el perro y el pez", 2) == [("el", 3), ("y", 2)]
    assert top_palabras("", 3) == []


def test_top_palabras_ignora_mayusculas():
    assert top_palabras("El el EL gato", 1) == [("el", 3)]


def test_top_palabras_n_mayor_al_total():
    assert top_palabras("uno dos", 10) == [("uno", 1), ("dos", 1)]


# 8 -------------------------------------------------------------------------
def test_repetidos():
    assert repetidos([1, 2, 2, 3, 3, 3]) == {2, 3}
    assert repetidos([1, 2, 3]) == set()
    assert repetidos([]) == set()
    assert repetidos(["a", "b", "a"]) == {"a"}


def test_repetidos_sin_count():
    """Esta vez tiene que ser O(n): nada de .count()."""
    cuerpo = inspect.getsource(repetidos).split('"""')[-1]
    # descartamos los comentarios, que no son código ejecutable
    codigo = "\n".join(linea.split("#")[0] for linea in cuerpo.splitlines())
    assert ".count(" not in codigo, "usá Counter, no .count()"


# 9 -------------------------------------------------------------------------
def test_agrupar_por_inicial():
    assert agrupar_por_inicial(["Ana", "Luis", "Alba"]) == {
        "A": ["Ana", "Alba"],
        "L": ["Luis"],
    }
    assert agrupar_por_inicial([]) == {}
    assert agrupar_por_inicial(["ana", "Alba"]) == {"A": ["ana", "Alba"]}


def test_agrupar_devuelve_dict_comun():
    """Un defaultdict inventa claves al consultarlas; un dict común no."""
    resultado = agrupar_por_inicial(["Ana"])
    assert type(resultado) is dict, "convertilo con dict(...) antes de devolverlo"
    with pytest.raises(KeyError):
        resultado["Z"]


# 10 ------------------------------------------------------------------------
def test_fusionar_config():
    assert fusionar_config({"host": "localhost", "puerto": 8000}, {"puerto": 9000}) == {
        "host": "localhost",
        "puerto": 9000,
    }
    assert fusionar_config({}, {"a": 1}) == {"a": 1}
    assert fusionar_config({"a": 1}, {}) == {"a": 1}


def test_fusionar_config_agrega_claves_nuevas():
    assert fusionar_config({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_fusionar_config_no_modifica_los_originales():
    default = {"puerto": 8000}
    usuario = {"puerto": 9000}
    fusionar_config(default, usuario)
    assert default == {"puerto": 8000}, "modificaste el dict que te pasaron"
    assert usuario == {"puerto": 9000}


# 11 ------------------------------------------------------------------------
def test_separar_cabecera():
    filas = [["id", "nombre"], [1, "Ana"], [2, "Luis"]]
    cabecera, resto = separar_cabecera(filas)
    assert cabecera == ["id", "nombre"]
    assert resto == [[1, "Ana"], [2, "Luis"]]


def test_separar_cabecera_sin_datos():
    cabecera, resto = separar_cabecera([["id", "nombre"]])
    assert cabecera == ["id", "nombre"]
    assert resto == []


def test_separar_cabecera_vacia():
    assert separar_cabecera([]) == ([], [])


def test_separar_cabecera_resto_es_lista():
    """`*resto` recoge una lista, no una tupla."""
    _, resto = separar_cabecera([["a"], ["b"]])
    assert isinstance(resto, list)
