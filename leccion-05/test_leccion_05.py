"""Tests de la Lección 05. NO los edites."""

import time

import pytest
from ejercicios_05 import (
    TAREAS,
    aplicar_a_resultado,
    cronometrar,
    duplica_despues_de_sumar,
    enviar_reporte,
    fib,
    limpiar_temporales,
    memorizar,
    registrar,
    repetir,
    sin_espacios,
    suma_despues_de_duplicar,
    validar_texto,
    valor_por_defecto,
)


# 1 -------------------------------------------------------------------------
def test_sin_espacios_limpia_el_resultado():
    @sin_espacios
    def leer_nombre():
        return "  Ana  "

    assert leer_nombre() == "Ana"


def test_sin_espacios_pasa_los_argumentos():
    @sin_espacios
    def unir(a, b, separador=" "):
        return f"  {a}{separador}{b}  "

    assert unir("Ana", "Perez", separador="-") == "Ana-Perez"


def test_sin_espacios_conserva_el_nombre():
    @sin_espacios
    def leer_nombre():
        return "x"

    assert leer_nombre.__name__ == "leer_nombre", "te falta @wraps(func)"


def test_sin_espacios_conserva_el_docstring():
    @sin_espacios
    def leer_nombre():
        """Lee un nombre."""
        return "x"

    assert leer_nombre.__doc__ == "Lee un nombre.", "te falta @wraps(func)"


# 2 -------------------------------------------------------------------------
def test_validar_texto_deja_pasar_lo_valido():
    @validar_texto
    def saludar(nombre):
        return f"Hola, {nombre}"

    assert saludar("Ana") == "Hola, Ana"


def test_validar_texto_rechaza_vacio():
    @validar_texto
    def saludar(nombre):
        return f"Hola, {nombre}"

    with pytest.raises(ValueError):
        saludar("")


def test_validar_texto_rechaza_solo_espacios():
    @validar_texto
    def saludar(nombre):
        return f"Hola, {nombre}"

    with pytest.raises(ValueError):
        saludar("   ")


def test_validar_texto_no_llega_a_llamar_la_funcion():
    """La guarda va antes de llamar, no después."""
    ejecuciones = []

    @validar_texto
    def saludar(nombre):
        ejecuciones.append(nombre)
        return f"Hola, {nombre}"

    with pytest.raises(ValueError):
        saludar("  ")
    assert ejecuciones == [], "validaste después de llamar a func"


# 3 -------------------------------------------------------------------------
def test_repetir_tres_veces():
    @repetir(3)
    def dado():
        return 4

    assert dado() == [4, 4, 4]


def test_repetir_una_vez():
    @repetir(1)
    def dado():
        return 4

    assert dado() == [4]


def test_repetir_cero_veces():
    @repetir(0)
    def dado():
        return 4

    assert dado() == []


def test_repetir_pasa_los_argumentos():
    @repetir(2)
    def doble(n, extra=0):
        return n * 2 + extra

    assert doble(5, extra=1) == [11, 11]


# 4 -------------------------------------------------------------------------
def test_valor_por_defecto_reemplaza_none():
    @valor_por_defecto("desconocido")
    def buscar_ciudad(id_):
        return None

    assert buscar_ciudad(7) == "desconocido"


def test_valor_por_defecto_deja_pasar_el_valor_real():
    @valor_por_defecto("desconocido")
    def buscar_ciudad(id_):
        return "Rosario"

    assert buscar_ciudad(7) == "Rosario"


def test_valor_por_defecto_no_reemplaza_el_cero():
    """0 es un resultado legítimo. Truthiness no sirve acá: hace falta `is None`."""

    @valor_por_defecto(-1)
    def contar():
        return 0

    assert contar() == 0


def test_valor_por_defecto_no_reemplaza_lo_vacio():
    @valor_por_defecto("desconocido")
    def leer():
        return ""

    assert leer() == ""


# 5 -------------------------------------------------------------------------
def test_duplica_despues_de_sumar():
    assert duplica_despues_de_sumar(5) == 12


def test_suma_despues_de_duplicar():
    assert suma_despues_de_duplicar(5) == 11


# 6 -------------------------------------------------------------------------
def test_registrar_llena_el_diccionario():
    assert set(TAREAS) >= {"limpiar_temporales", "enviar_reporte"}


def test_registrar_devuelve_la_funcion_intacta():
    assert TAREAS["limpiar_temporales"] is limpiar_temporales, (
        "el registro tiene que guardar la función misma, no un envoltorio"
    )


def test_registrar_no_envuelve():
    assert limpiar_temporales.__name__ == "limpiar_temporales"
    assert enviar_reporte("ana@mail.com") == "reporte enviado a ana@mail.com"


def test_registrar_usa_el_nombre_de_la_funcion():
    @registrar
    def tarea_nueva():
        return "ok"

    assert TAREAS["tarea_nueva"] is tarea_nueva


# 7 -------------------------------------------------------------------------
def test_memorizar_devuelve_lo_mismo():
    @memorizar
    def cuadrado(n):
        return n * n

    assert cuadrado(4) == 16


def test_memorizar_no_recalcula():
    ejecuciones = []

    @memorizar
    def cuadrado(n):
        ejecuciones.append(n)
        return n * n

    cuadrado(4)
    cuadrado(4)
    cuadrado(4)
    assert ejecuciones == [4], (
        "el cuerpo se ejecutó más de una vez para el mismo argumento"
    )


def test_memorizar_distingue_los_argumentos():
    ejecuciones = []

    @memorizar
    def cuadrado(n):
        ejecuciones.append(n)
        return n * n

    assert (cuadrado(2), cuadrado(3), cuadrado(2)) == (4, 9, 4)
    assert ejecuciones == [2, 3]


def test_memorizar_conserva_el_nombre():
    @memorizar
    def cuadrado(n):
        return n * n

    assert cuadrado.__name__ == "cuadrado", "te falta @wraps(func)"


# 8 -------------------------------------------------------------------------
def test_fib_valores():
    assert (fib(0), fib(1), fib(10)) == (0, 1, 55)


def test_fib_esta_cacheada():
    assert hasattr(fib, "cache_info"), "le falta el decorador de functools"


def test_fib_es_rapida():
    """Sin caché, fib(35) tarda segundos."""
    arranque = time.perf_counter()
    assert fib(35) == 9227465
    assert time.perf_counter() - arranque < 0.5


# 9 -------------------------------------------------------------------------
def test_cronometrar_devuelve_el_resultado():
    @cronometrar
    def trabajar():
        return "listo"

    assert trabajar() == "listo"


def test_cronometrar_guarda_la_duracion():
    @cronometrar
    def trabajar():
        return "listo"

    trabajar()
    assert isinstance(trabajar.ultima_duracion, float)


def test_cronometrar_mide_algo_mayor_a_cero():
    @cronometrar
    def trabajo_pesado():
        return sum(range(200_000))

    trabajo_pesado()
    assert trabajo_pesado.ultima_duracion > 0


def test_cronometrar_conserva_el_nombre():
    @cronometrar
    def trabajar():
        return "listo"

    assert trabajar.__name__ == "trabajar", "te falta @wraps(func)"


# 10 ------------------------------------------------------------------------
def test_aplicar_a_resultado_con_upper():
    @aplicar_a_resultado(str.upper)
    def leer():
        return "hola"

    assert leer() == "HOLA"


def test_aplicar_a_resultado_con_len():
    @aplicar_a_resultado(len)
    def listar():
        return [1, 2, 3]

    assert listar() == 3


def test_aplicar_a_resultado_reemplaza_a_sin_espacios():
    """`sin_espacios` es un caso particular de este decorador."""
    quitar_espacios = aplicar_a_resultado(str.strip)

    @quitar_espacios
    def generico():
        return "  Ana  "

    @sin_espacios
    def especifico():
        return "  Ana  "

    assert generico() == especifico() == "Ana"
