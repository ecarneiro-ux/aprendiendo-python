"""Tests de la Lección 01. NO los edites — están para decirte si tu código funciona."""

import pytest
from ejercicios_01 import (
    agregar_al_carrito,
    clasificar_nota,
    contar_caracteres,
    describir,
    es_palindromo,
    intercambiar,
    presentar,
    primera_palabra_larga,
    segundos_a_hms,
    ultimos,
)


# 1 -------------------------------------------------------------------------
def test_presentar():
    assert presentar("Ana", 30) == "Hola, me llamo Ana y tengo 30 años."
    assert presentar("Emiliano", 1) == "Hola, me llamo Emiliano y tengo 1 años."


# 2 -------------------------------------------------------------------------
@pytest.mark.parametrize("valor", [0, "", [], {}, set(), None, 0.0, False])
def test_describir_falsy(valor):
    assert describir(valor) == "vacío"


@pytest.mark.parametrize("valor", [1, "hola", [0], {"a": 1}, -5, True, 0.1])
def test_describir_truthy(valor):
    assert describir(valor) == "con contenido"


# 3 -------------------------------------------------------------------------
def test_intercambiar():
    assert intercambiar(1, 2) == (2, 1)
    assert intercambiar("a", "b") == ("b", "a")
    assert intercambiar(None, [1]) == ([1], None)


# 4 -------------------------------------------------------------------------
@pytest.mark.parametrize(
    "total,esperado",
    [
        (0, (0, 0, 0)),
        (59, (0, 0, 59)),
        (60, (0, 1, 0)),
        (3725, (1, 2, 5)),
        (86399, (23, 59, 59)),
        (90061, (25, 1, 1)),  # más de un día: NO se reinicia
    ],
)
def test_segundos_a_hms(total, esperado):
    assert segundos_a_hms(total) == esperado


# 5 -------------------------------------------------------------------------
def test_ultimos():
    assert ultimos([1, 2, 3, 4, 5], 2) == [4, 5]
    assert ultimos([1, 2, 3], 3) == [1, 2, 3]
    assert ultimos([1, 2, 3], 10) == [1, 2, 3]
    assert ultimos([], 3) == []


def test_ultimos_cero():
    """El caso borde: n=0 debe dar lista vacía, no la lista entera."""
    assert ultimos([1, 2, 3], 0) == []


# 6 -------------------------------------------------------------------------
@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("Anita lava la tina", True),
        ("neuquen", True),
        ("Somos o no somos", True),
        ("hola", False),
        ("", True),
        ("a", True),
        ("Ana", True),
    ],
)
def test_es_palindromo(texto, esperado):
    assert es_palindromo(texto) is esperado


# 7 -------------------------------------------------------------------------
def test_carrito_nuevo_cada_vez():
    """Si esto falla, caíste en la trampa del default mutable."""
    assert agregar_al_carrito("pan") == ["pan"]
    assert agregar_al_carrito("leche") == ["leche"]
    assert agregar_al_carrito("queso") == ["queso"]


def test_carrito_existente():
    carrito = ["pan"]
    resultado = agregar_al_carrito("leche", carrito)
    assert resultado == ["pan", "leche"]
    assert resultado is carrito  # debe modificar el mismo carrito, no una copia


# 8 -------------------------------------------------------------------------
@pytest.mark.parametrize(
    "nota,esperado",
    [
        (10, "excelente"),
        (9, "excelente"),
        (8, "aprobado"),
        (7, "aprobado"),
        (6, "regular"),
        (4, "regular"),
        (3, "insuficiente"),
        (0, "insuficiente"),
        (11, "inválida"),
        (-1, "inválida"),
    ],
)
def test_clasificar_nota(nota, esperado):
    assert clasificar_nota(nota) == esperado


# 9 -------------------------------------------------------------------------
def test_primera_palabra_larga():
    assert primera_palabra_larga("el gato negro duerme", 4) == "negro"
    assert primera_palabra_larga("uno dos tres", 2) == "uno"
    assert primera_palabra_larga("a bb ccc", 10) is None
    assert primera_palabra_larga("", 1) is None


def test_primera_palabra_larga_es_estricto():
    """'MÁS de minimo', no 'al menos minimo'."""
    assert primera_palabra_larga("casa hogar", 4) == "hogar"


# 10 ------------------------------------------------------------------------
def test_contar_caracteres():
    assert contar_caracteres("casa") == {"c": 1, "a": 2, "s": 1}
    assert contar_caracteres("") == {}
    assert contar_caracteres("aaa") == {"a": 3}


def test_contar_caracteres_ignora_espacios():
    assert contar_caracteres("a b a") == {"a": 2, "b": 1}
