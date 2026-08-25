"""Tests de la Lección 04. NO los edites."""

import inspect

import pytest
from ejercicios_04 import (
    aplicar_a_todos,
    calcular,
    contar_llamadas,
    crear_url,
    crear_usuario,
    describir,
    hacer_multiplicador,
    hacer_redondeador,
    hacer_validador,
    llamar_con,
    ordenador_por,
    promedio,
)

CATALOGO = [
    {"nombre": "teclado", "categoria": "accesorio", "precio": 50},
    {"nombre": "monitor", "categoria": "pantalla", "precio": 300},
    {"nombre": "mouse", "categoria": "accesorio", "precio": 20},
    {"nombre": "tablet", "categoria": "pantalla", "precio": 150},
]


# 1 -------------------------------------------------------------------------
def test_promedio():
    assert promedio(1, 2, 3) == 2.0
    assert promedio(10) == 10.0


def test_promedio_sin_argumentos():
    """La guarda va ANTES de dividir, no después."""
    assert promedio() == 0.0


def test_promedio_recibe_sueltos_no_una_lista():
    """Con *args, promedio([1, 2, 3]) NO es una llamada válida de números."""
    firma = inspect.signature(promedio)
    tipos = [p.kind for p in firma.parameters.values()]
    assert inspect.Parameter.VAR_POSITIONAL in tipos, "te falta el * en la firma"


# 2 -------------------------------------------------------------------------
def test_describir():
    assert describir(peso=3, color="rojo") == "color=rojo; peso=3"


def test_describir_ordena_alfabeticamente():
    assert describir(z=1, a=2, m=3) == "a=2; m=3; z=1"


def test_describir_uno_solo_no_lleva_separador():
    assert describir(color="rojo") == "color=rojo"


def test_describir_vacio():
    assert describir() == ""


# 3 -------------------------------------------------------------------------
def test_crear_url():
    assert (
        crear_url("https://api.com/datos", pagina=2, orden="asc")
        == "https://api.com/datos?orden=asc&pagina=2"
    )


def test_crear_url_sin_params_no_lleva_interrogacion():
    assert crear_url("https://api.com/datos") == "https://api.com/datos"


def test_crear_url_un_solo_param():
    assert crear_url("http://x", id=7) == "http://x?id=7"


# 4 -------------------------------------------------------------------------
def test_crear_usuario_por_nombre():
    assert crear_usuario("ana", admin=True) == {
        "nombre": "ana",
        "admin": True,
        "activo": True,
    }


def test_crear_usuario_defaults():
    assert crear_usuario("luis") == {"nombre": "luis", "admin": False, "activo": True}


def test_crear_usuario_no_acepta_posicionales():
    """Este es el punto del ejercicio: hay que agregar el * a la firma."""
    with pytest.raises(TypeError):
        crear_usuario("ana", True)


def test_crear_usuario_nombre_puede_ir_posicional_o_por_nombre():
    assert crear_usuario("ana") == crear_usuario(nombre="ana")


# 5 -------------------------------------------------------------------------
def test_llamar_con_posicionales():
    assert llamar_con(max, [3, 9, 1], {}) == 9


def test_llamar_con_nombrados():
    assert llamar_con(round, [3.14159], {"ndigits": 2}) == 3.14


def test_llamar_con_mezcla():
    def f(a, b, c=0, d=0):
        return (a, b, c, d)

    assert llamar_con(f, [1, 2], {"d": 4}) == (1, 2, 0, 4)


def test_llamar_con_sin_nada():
    assert llamar_con(dict, [], {}) == {}


# 6 -------------------------------------------------------------------------
def test_aplicar_a_todos():
    assert aplicar_a_todos(len, ["hola", "chau", "a"]) == [4, 4, 1]


def test_aplicar_a_todos_vacio():
    assert aplicar_a_todos(len, []) == []


def test_aplicar_a_todos_con_lambda():
    assert aplicar_a_todos(lambda x: x * 2, [1, 2, 3]) == [2, 4, 6]


def test_aplicar_a_todos_no_modifica_el_original():
    original = [1, 2, 3]
    aplicar_a_todos(lambda x: x * 2, original)
    assert original == [1, 2, 3]


# 7 -------------------------------------------------------------------------
def test_calcular():
    assert calcular("sumar", 2, 3) == 5
    assert calcular("restar", 10, 4) == 6
    assert calcular("multiplicar", 3, 4) == 12
    assert calcular("maximo", 3, 9) == 9


def test_calcular_operacion_inexistente():
    assert calcular("potencia", 2, 3) is None


def test_calcular_sin_cadena_de_elif():
    fuente = inspect.getsource(calcular)
    assert "elif" not in fuente, (
        "el punto del ejercicio es el dict de funciones, no la cadena de if/elif"
    )


# 8 -------------------------------------------------------------------------
def test_hacer_multiplicador():
    doble = hacer_multiplicador(2)
    assert doble(5) == 10
    assert doble(0) == 0


def test_hacer_multiplicador_devuelve_una_funcion():
    assert callable(hacer_multiplicador(2)), "devolviste un valor, no una función"


def test_multiplicadores_independientes():
    doble = hacer_multiplicador(2)
    triple = hacer_multiplicador(3)
    assert (doble(10), triple(10)) == (20, 30)


# 9 -------------------------------------------------------------------------
def test_hacer_validador():
    es_edad_valida = hacer_validador(0, 120)
    assert es_edad_valida(30) is True
    assert es_edad_valida(150) is False


def test_hacer_validador_incluye_los_bordes():
    entre = hacer_validador(10, 20)
    assert entre(10) is True
    assert entre(20) is True
    assert entre(9) is False
    assert entre(21) is False


def test_hacer_validador_sirve_como_filtro():
    entre = hacer_validador(1, 3)
    assert [n for n in [0, 1, 2, 3, 4] if entre(n)] == [1, 2, 3]


# 10 ------------------------------------------------------------------------
def test_contar_llamadas_arranca_en_cero():
    contado = contar_llamadas(str.upper)
    assert contado.llamadas == 0


def test_contar_llamadas_devuelve_lo_mismo_que_la_original():
    contado = contar_llamadas(str.upper)
    assert contado("hola") == "HOLA"


def test_contar_llamadas_cuenta():
    contado = contar_llamadas(str.upper)
    contado("a")
    contado("b")
    contado("c")
    assert contado.llamadas == 3


def test_contar_llamadas_acepta_cualquier_firma():
    def f(a, b=0, *extras, clave=None, **resto):
        return (a, b, extras, clave, resto)

    contado = contar_llamadas(f)
    assert contado(1, 2, 3, 4, clave="x", otro=9) == (1, 2, (3, 4), "x", {"otro": 9})
    assert contado.llamadas == 1


def test_contar_llamadas_cada_envoltorio_lleva_su_cuenta():
    uno = contar_llamadas(str.upper)
    otro = contar_llamadas(str.upper)
    uno("a")
    uno("b")
    otro("c")
    assert (uno.llamadas, otro.llamadas) == (2, 1)


def test_contar_llamadas_no_toca_la_funcion_original():
    def f(x):
        return x

    contado = contar_llamadas(f)
    contado(1)
    assert not hasattr(f, "llamadas"), "le colgaste el contador a la función original"


# 11 ------------------------------------------------------------------------
def test_hacer_redondeador():
    a_centavos = hacer_redondeador(2)
    assert a_centavos(3.14159) == 3.14
    assert a_centavos(2.005001) == 2.01


def test_hacer_redondeador_cero_decimales():
    entero = hacer_redondeador(0)
    assert entero(3.7) == 4


def test_hacer_redondeador_usa_partial():
    fuente = inspect.getsource(hacer_redondeador)
    assert "partial" in fuente, "el ejercicio es resolverlo con functools.partial"


# 12 ------------------------------------------------------------------------
def test_ordenador_por_una_clave():
    por_edad = ordenador_por("edad")
    assert por_edad([{"edad": 30}, {"edad": 25}]) == [{"edad": 25}, {"edad": 30}]


def test_ordenador_por_dos_claves():
    ordenar_catalogo = ordenador_por("categoria", "precio")
    assert [p["nombre"] for p in ordenar_catalogo(CATALOGO)] == [
        "mouse",
        "teclado",
        "tablet",
        "monitor",
    ]


def test_ordenador_por_devuelve_una_funcion():
    assert callable(ordenador_por("edad"))


def test_ordenador_por_no_modifica_el_original():
    catalogo = list(CATALOGO)
    ordenador_por("precio")(catalogo)
    assert catalogo == list(CATALOGO), "usaste .sort() en vez de sorted()"


def test_ordenador_por_lista_vacia():
    assert ordenador_por("edad")([]) == []


def test_ordenadores_independientes():
    por_precio = ordenador_por("precio")
    por_nombre = ordenador_por("nombre")
    assert por_precio(CATALOGO)[0]["nombre"] == "mouse"
    assert por_nombre(CATALOGO)[0]["nombre"] == "monitor"
