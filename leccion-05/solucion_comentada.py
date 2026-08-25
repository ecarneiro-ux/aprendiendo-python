"""
Lección 05 — Solución de referencia.

LEÉ ESTO SOLO DESPUÉS de tener tus 36 tests en verde.
"""

from functools import cache, wraps
from time import perf_counter


def sin_espacios(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs).strip()

    return envoltorio


def validar_texto(func):
    # También lleva @wraps: la regla es "todo envoltorio lo lleva".
    # Que no haya un test que lo verifique no lo hace opcional.
    @wraps(func)
    def envoltorio(*args, **kwargs):
        if not args[0].strip():
            raise ValueError("el texto no puede estar vacío")
        return func(*args, **kwargs)

    return envoltorio


def repetir(veces: int):
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(veces)]

        return envoltorio

    return decorador


def valor_por_defecto(reemplazo):
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            # UNA sola llamada, guardada en una variable.
            # Llamar dos veces (una para el if y otra para el return) no es
            # "un poco más lento": es un bug. Si `func` escribe en una base,
            # manda un mail o devuelve algo distinto cada vez, el resultado
            # que verificaste no es el que devolvés.
            resultado = func(*args, **kwargs)
            if resultado is None:
                return reemplazo
            return resultado

        return envoltorio

    return decorador


def duplicar(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs) * 2

    return envoltorio


def sumar_uno(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs) + 1

    return envoltorio


# Se aplican de abajo hacia arriba: el de abajo queda adentro.
#   duplica_despues_de_sumar = duplicar(sumar_uno(func))
@duplicar
@sumar_uno
def duplica_despues_de_sumar(n: int) -> int:
    return n


@sumar_uno
@duplicar
def suma_despues_de_duplicar(n: int) -> int:
    return n


TAREAS: dict = {}


def registrar(func):
    # No hay envoltorio: el efecto pasa al DECORAR, no al llamar.
    # Por eso tampoco hace falta wraps. Así funciona @app.get() de FastAPI.
    TAREAS[func.__name__] = func
    return func


@registrar
def limpiar_temporales() -> str:
    return "temporales limpiados"


@registrar
def enviar_reporte(destino: str) -> str:
    return f"reporte enviado a {destino}"


def memorizar(func):
    # El dict del caché se crea UNA vez, al decorar. El closure lo mantiene
    # vivo entre llamadas.
    resultados = {}

    @wraps(func)
    def envoltorio(*args):
        # `args` YA es una tupla y ya es hashable: sirve tal cual como clave,
        # y así funciona con cualquier cantidad de argumentos, no solo uno.
        #
        # No hace falta una lista aparte con las claves ya vistas: las claves
        # del dict SON ese registro. Preguntarle al dict es O(1); recorrer una
        # lista paralela es O(n) y encima puede desincronizarse.
        if args not in resultados:
            resultados[args] = func(*args)
        return resultados[args]

    return envoltorio


# `@cache` es exactamente lo de arriba, escrito por otro y mejor probado.
# Guarda un dict {argumentos: resultado} y trae .cache_info() / .cache_clear().
@cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def cronometrar(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        arranque = perf_counter()
        # Hay que guardar el resultado: con `return func(...)` directo, la
        # función sale antes de poder tomar la segunda medición.
        resultado = func(*args, **kwargs)
        envoltorio.ultima_duracion = perf_counter() - arranque  # type: ignore[attr-defined]
        return resultado

    # Inicializarlo está bien: el atributo existe desde el momento en que se
    # decora, no recién después de la primera llamada. Pero que sea 0.0 y no
    # 0 — el tipo del atributo no debería cambiar de int a float sola.
    envoltorio.ultima_duracion = 0.0  # type: ignore[attr-defined]
    return envoltorio


def aplicar_a_resultado(transformacion):
    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            return transformacion(func(*args, **kwargs))

        return envoltorio

    return decorador


# Y acá el ejercicio 1 desaparece: es un caso particular del 10.
sin_espacios_v2 = aplicar_a_resultado(str.strip)


if __name__ == "__main__":
    print(TAREAS)
    print(fib(35), fib.cache_info())

    @aplicar_a_resultado(str.upper)
    def leer():
        return "hola"

    print(leer())
