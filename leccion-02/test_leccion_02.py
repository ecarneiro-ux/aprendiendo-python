"""Tests de la Lección 02. NO los edites."""

import pytest
from ejercicios_02 import (
    agrupar_por_inicial,
    aplanar,
    combinar,
    con_stock,
    cuadrados,
    elementos_comunes,
    normalizar,
    palabras_unicas,
    posiciones,
    repetidos,
    solo_pares,
)


# 1 -------------------------------------------------------------------------
def test_cuadrados():
    assert cuadrados(5) == [0, 1, 4, 9, 16]
    assert cuadrados(1) == [0]
    assert cuadrados(0) == []


# 2 -------------------------------------------------------------------------
def test_solo_pares():
    assert solo_pares([1, 2, 3, 4, 5, 6]) == [2, 4, 6]
    assert solo_pares([1, 3, 5]) == []
    assert solo_pares([]) == []


def test_solo_pares_incluye_el_cero_y_negativos():
    assert solo_pares([0, -2, -3]) == [0, -2]


# 3 -------------------------------------------------------------------------
def test_normalizar():
    assert normalizar(["  ana perez ", "", "LUIS GOMEZ", "   "]) == [
        "Ana Perez",
        "Luis Gomez",
    ]


def test_normalizar_descarta_solo_espacios():
    """'   ' no está vacío como string, pero después del .strip() sí."""
    assert normalizar(["   ", "\t", "ok"]) == ["Ok"]
    assert normalizar([]) == []


# 4 -------------------------------------------------------------------------
def test_posiciones():
    assert posiciones(["a", "b", "c"]) == {"a": 0, "b": 1, "c": 2}
    assert posiciones([]) == {}


def test_posiciones_repetidos_gana_el_ultimo():
    assert posiciones(["a", "b", "a"]) == {"a": 2, "b": 1}


# 5 -------------------------------------------------------------------------
def test_combinar():
    assert combinar(["a", "b"], [1, 2]) == {"a": 1, "b": 2}
    assert combinar([], []) == {}


def test_combinar_largos_distintos():
    assert combinar(["a", "b", "c"], [1, 2]) == {"a": 1, "b": 2}
    assert combinar(["a"], [1, 2, 3]) == {"a": 1}


# 6 -------------------------------------------------------------------------
def test_palabras_unicas():
    assert palabras_unicas("El gato y el Gato") == {"el", "gato", "y"}
    assert palabras_unicas("") == set()
    assert palabras_unicas("uno") == {"uno"}


# 7 -------------------------------------------------------------------------
def test_elementos_comunes():
    assert elementos_comunes([1, 2, 3], [2, 3, 4]) == {2, 3}
    assert elementos_comunes([1, 2], [3, 4]) == set()
    assert elementos_comunes([], [1]) == set()


def test_elementos_comunes_no_repite():
    assert elementos_comunes([1, 1, 2], [1, 1, 1]) == {1}


# 8 -------------------------------------------------------------------------
def test_repetidos():
    assert repetidos([1, 2, 2, 3, 3, 3]) == {2, 3}
    assert repetidos([1, 2, 3]) == set()
    assert repetidos([]) == set()


def test_repetidos_con_strings():
    assert repetidos(["a", "b", "a", "c", "b"]) == {"a", "b"}


# 9 -------------------------------------------------------------------------
def test_aplanar():
    assert aplanar([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
    assert aplanar([]) == []


def test_aplanar_con_sublistas_vacias():
    assert aplanar([[], [1], []]) == [1]


# 10 ------------------------------------------------------------------------
def test_con_stock():
    assert con_stock({"pan": 3, "leche": 0, "queso": 7}) == {"pan": 3, "queso": 7}
    assert con_stock({}) == {}
    assert con_stock({"a": 0}) == {}


def test_con_stock_descarta_negativos():
    assert con_stock({"a": -5, "b": 1}) == {"b": 1}


# 11 ------------------------------------------------------------------------
def test_agrupar_por_inicial():
    assert agrupar_por_inicial(["Ana", "Luis", "Alba"]) == {
        "A": ["Ana", "Alba"],
        "L": ["Luis"],
    }
    assert agrupar_por_inicial([]) == {}


def test_agrupar_por_inicial_normaliza_mayuscula():
    assert agrupar_por_inicial(["ana", "Alba"]) == {"A": ["ana", "Alba"]}


def test_agrupar_por_inicial_respeta_el_orden():
    resultado = agrupar_por_inicial(["Bob", "Ana", "Beto"])
    assert resultado["B"] == ["Bob", "Beto"]


# Chequeo de estilo -----------------------------------------------------------
@pytest.mark.parametrize(
    "funcion",
    [cuadrados, solo_pares, normalizar, posiciones, combinar, palabras_unicas, aplanar],
)
def test_sin_append(funcion):
    """Estas siete se resuelven con comprehensions. Si usaste .append(), rehacelas.

    (El 11 sí puede usarlo, por eso no está en la lista.)
    """
    import inspect

    codigo = inspect.getsource(funcion)
    cuerpo = codigo.split('"""')[-1]  # descartamos el docstring
    assert ".append(" not in cuerpo, (
        f"{funcion.__name__} usa .append() — resolvelo con una comprehension"
    )
