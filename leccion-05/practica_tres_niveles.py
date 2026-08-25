"""
Práctica: decoradores CON parámetros (los tres niveles).

Seis ejercicios cortos del mismo patrón, de menor a mayor.
No son parte de la lección: no hay tests de pytest, se corrige este archivo solo.

    python leccion-05/practica_tres_niveles.py

La idea es hacerlos SIN abrir teoria.md. Si te trabás, abajo de todo hay un
molde vacío (buscá "RED DE SEGURIDAD"), pero probá de memoria primero: la
repetición es lo que fija el patrón.

Los seis piden `@wraps(func)`. Va siempre, y el corrector lo verifica.
"""

from functools import wraps  # noqa: F401  (lo vas a usar en los seis)


# ===========================================================================
# 1. multiplicar_resultado(factor)
# ===========================================================================
# Multiplica por `factor` lo que devuelva la función.
#
#     @multiplicar_resultado(3)
#     def base():
#         return 10
#
#     base()  # 30
def multiplicar_resultado(factor):
    # escribí acá: tres niveles, tres return
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            return func(*args, **kwargs) * factor

        return envoltorio

    return decorador


# ===========================================================================
# 2. agregar_sufijo(sufijo)
# ===========================================================================
# Le pega `sufijo` al string que devuelva la función.
#
#     @agregar_sufijo(" (borrador)")
#     def titulo():
#         return "Informe anual"
#
#     titulo()  # 'Informe anual (borrador)'
def agregar_sufijo(sufijo):
    # escribí acá: tres niveles, tres return
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            return func(*args, **kwargs) + sufijo

        return envoltorio

    return decorador


# ===========================================================================
# 3. limitar(maximo)
# ===========================================================================
# Si el resultado supera `maximo`, devolvé `maximo`. Si no, el resultado.
# Acá el envoltorio tiene lógica adentro, no solo una transformación.
#
#     @limitar(100)
#     def puntaje(n):
#         return n * 10
#
#     puntaje(5)   # 50
#     puntaje(50)  # 100
def limitar(maximo):
    # escribí acá: tres niveles, tres return
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            valor_funcion = func(*args, **kwargs)
            return min(valor_funcion, maximo)

        return envoltorio

    return decorador


# ===========================================================================
# 4. saltear_si(prohibido)
# ===========================================================================
# Si el PRIMER argumento posicional es igual a `prohibido`, devolvé None
# SIN llamar a la función. Si no, comportamiento normal.
#
# (Mismo molde que el ejercicio 2 de la lección, pero con parámetro: la guarda
# va antes de llamar a func.)
#
#     @saltear_si("admin")
#     def borrar_usuario(nombre):
#         return f"{nombre} borrado"
#
#     borrar_usuario("ana")    # 'ana borrado'
#     borrar_usuario("admin")  # None
def saltear_si(prohibido):
    # escribí acá: tres niveles, tres return
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            if args[0] == prohibido:
                return None
            return func(*args, **kwargs)

        return envoltorio

    return decorador


# ===========================================================================
# 5. contar_en(registro)
# ===========================================================================
# El parámetro no es un número ni un string: es una LISTA. Cada vez que se
# llame a la función, agregale a esa lista el nombre de la función.
# Devolvé el resultado normal.
#
# Pista: el nombre está en `func.__name__`, y una lista se muta con .append()
# (no hace falta `nonlocal` para eso).
#
#     historial = []
#
#     @contar_en(historial)
#     def guardar():
#         return "ok"
#
#     guardar()
#     guardar()
#     historial  # ['guardar', 'guardar']
def contar_en(registro):
    # escribí acá: tres niveles, tres return
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            registro.append(func.__name__)
            return func(*args, **kwargs)

        return envoltorio

    return decorador


# ===========================================================================
# 6. envolver_entre(izquierda, derecha)
# ===========================================================================
# Dos parámetros. Devolvé el resultado con esos textos pegados a cada lado.
#
#     @envolver_entre("<b>", "</b>")
#     def texto():
#         return "hola"
#
#     texto()  # '<b>hola</b>'
def envolver_entre(izquierda, derecha):
    # escribí acá: tres niveles, tres return
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            return izquierda + func(*args, **kwargs) + derecha

        return envoltorio

    return decorador


# ===========================================================================
# De acá para abajo no toques nada: es el que te corrige.
# ===========================================================================
def comparar(obtenido, esperado):
    if obtenido == esperado:
        return True, "funciona"
    if obtenido is None:
        return False, "devolviste None. Falta un `return` en alguno de los niveles."
    return False, f"devolviste {obtenido!r} y se esperaba {esperado!r}."


def con_nombre(decorada, esperado_nombre, resultado):
    """Combina el chequeo de comportamiento con el de @wraps."""
    ok, detalle = resultado
    if not ok:
        return ok, detalle
    if decorada.__name__ != esperado_nombre:
        return False, (
            f"anda, pero __name__ vale {decorada.__name__!r}.\n"
            f"{'':>36}Falta @wraps(func) arriba del envoltorio."
        )
    return True, "funciona y conserva el nombre"


def revisar(numero, titulo, prueba):
    try:
        ok, detalle = prueba()
    except TypeError as e:
        if "not callable" in str(e):
            detalle = (
                f"TypeError: {e}\n"
                f"{'':>36}Tu fabrica no devolvio un decorador usable.\n"
                f"{'':>36}Contá los niveles: parametros -> funcion -> argumentos,\n"
                f"{'':>36}y que cada uno devuelva el de abajo."
            )
        else:
            detalle = f"TypeError: {e}"
        ok = False
    except Exception as e:  # noqa: BLE001  (es el corrector: acá quiero atrapar todo)
        ok, detalle = False, f"{type(e).__name__}: {e}"
    print(f"{numero}. {titulo:<24} {'OK   ' if ok else 'FALLA'}  {detalle}")
    return ok


def probar_1():
    @multiplicar_resultado(3)
    def base():
        return 10

    return con_nombre(base, "base", comparar(base(), 30))


def probar_2():
    @agregar_sufijo(" (borrador)")
    def titulo():
        return "Informe anual"

    return con_nombre(titulo, "titulo", comparar(titulo(), "Informe anual (borrador)"))


def probar_3():
    @limitar(100)
    def puntaje(n):
        return n * 10

    ok, detalle = comparar(puntaje(5), 50)
    if not ok:
        return ok, detalle
    return con_nombre(puntaje, "puntaje", comparar(puntaje(50), 100))


def probar_4():
    ejecuciones = []

    @saltear_si("admin")
    def borrar_usuario(nombre):
        ejecuciones.append(nombre)
        return f"{nombre} borrado"

    ok, detalle = comparar(borrar_usuario("ana"), "ana borrado")
    if not ok:
        return ok, detalle
    if borrar_usuario("admin") is not None:
        return False, "con el valor prohibido tenés que devolver None."
    if "admin" in ejecuciones:
        return False, "llamaste a func igual: la guarda va ANTES de llamarla."
    return con_nombre(borrar_usuario, "borrar_usuario", (True, ""))


def probar_5():
    historial = []

    @contar_en(historial)
    def guardar():
        return "ok"

    ok, detalle = comparar(guardar(), "ok")
    if not ok:
        return ok, detalle
    guardar()
    if historial != ["guardar", "guardar"]:
        return (
            False,
            f"el registro quedó en {historial!r} y se esperaba ['guardar', 'guardar'].",
        )
    return con_nombre(guardar, "guardar", (True, ""))


def probar_6():
    @envolver_entre("<b>", "</b>")
    def texto():
        return "hola"

    return con_nombre(texto, "texto", comparar(texto(), "<b>hola</b>"))


if __name__ == "__main__":
    print("=" * 78)
    resultados = [
        revisar(1, "multiplicar_resultado", probar_1),
        revisar(2, "agregar_sufijo", probar_2),
        revisar(3, "limitar", probar_3),
        revisar(4, "saltear_si", probar_4),
        revisar(5, "contar_en", probar_5),
        revisar(6, "envolver_entre", probar_6),
    ]
    print("=" * 78)
    print(f"{sum(resultados)}/6")
    if all(resultados):
        print("Listo. Volvé al ejercicio 4 de la lección: es este mismo molde.")


# ===========================================================================
# RED DE SEGURIDAD — abrí esto solo si después de intentarlo no sale
# ===========================================================================
#
# El molde, vacío:
#
#     def fabrica(PARAMETRO):              # nivel 1: los parámetros del @
#         def decorador(func):             # nivel 2: la función decorada
#             @wraps(func)
#             def envoltorio(*args, **kwargs):   # nivel 3: cada llamada
#                 resultado = func(*args, **kwargs)
#                 return resultado         # ...transformado con PARAMETRO
#
#             return envoltorio            # el 2 devuelve el 3
#
#         return decorador                 # el 1 devuelve el 2
#
# Las tres líneas que más se olvidan son los tres `return`. Si alguno falta,
# el error que ves es "'NoneType' object is not callable".
