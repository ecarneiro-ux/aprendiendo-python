"""
Lección 05 — Decoradores.

Completá cada función reemplazando el `...` por tu código.
Corré los tests con:  pytest leccion-05 -v

Antes de arrancar:  python leccion-05/demo_decoradores.py

Los ejercicios 7 y 8 son el mismo problema resuelto dos veces: primero a mano,
después con una línea. El 10 se come al 1.
"""

from functools import cache, wraps
from time import perf_counter


# ---------------------------------------------------------------------------
# 1. El decorador mínimo
# ---------------------------------------------------------------------------
def sin_espacios(func):
    """Decorador: le saca los espacios de los bordes al string que devuelve `func`.

    Requisitos (valen para TODOS los decoradores de esta lección):
      - el envoltorio acepta cualquier firma
      - devuelve lo que devuelve la original, transformado
      - lleva `@wraps(func)` — hay un test que lo verifica

    Uso:
        @sin_espacios
        def leer_nombre():
            return "  Ana  "

        leer_nombre()  # 'Ana'
    """

    @wraps(func)
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs).strip()

    return envoltorio


# ---------------------------------------------------------------------------
# 2. Un decorador que valida (y corta con raise)
# ---------------------------------------------------------------------------
def validar_texto(func):
    """Decorador: revisa el PRIMER argumento posicional antes de llamar a `func`.

    Si ese argumento es un string vacío o de puros espacios, lanzá
    `ValueError`. Si está bien, llamá a `func` normalmente y devolvé lo suyo.

    La guarda va ANTES de llamar a `func` — ese es todo el punto de validar.

    Uso:
        @validar_texto
        def saludar(nombre):
            return f"Hola, {nombre}"

        saludar("Ana")  # 'Hola, Ana'
        saludar("   ")  # ValueError
    """
    @wraps(func)
    def envoltorio(*args, **kwargs):
        if not args[0].strip():
            raise ValueError("El argumento es un string vacío o de puros espacios")
        return func(*args, **kwargs)

    return envoltorio


# ---------------------------------------------------------------------------
# 3. Decorador con parámetros (los tres niveles)
# ---------------------------------------------------------------------------
def repetir(veces: int):
    """Fábrica de decoradores: hace que la función se ejecute `veces` veces y
    devuelve la LISTA de resultados.

    Ojo con la cantidad de niveles. Releé la sección 4 y desazucará mentalmente:
        f = repetir(3)(f)

    Uso:
        @repetir(3)
        def dado():
            return 4

        dado()  # [4, 4, 4]

    Con `veces=0` la lista sale vacía.
            # for _ in range(veces):
            #     valor = func(*args, **kwargs)
            #     resultados.append(valor)
            # return resultados
    """

    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(veces)]

        return envoltorio

    return decorador


# ---------------------------------------------------------------------------
# 4. Otro con parámetros — y una trampa de truthiness
# ---------------------------------------------------------------------------
def valor_por_defecto(reemplazo):
    """Fábrica de decoradores: si `func` devuelve None, devolvé `reemplazo`.

    ⚠️ SOLO None se reemplaza. Si la función devuelve 0, "" o [], esos son
    resultados legítimos y tienen que pasar tal cual. Hay tests para eso.

    Uso:
        @valor_por_defecto("desconocido")
        def buscar_ciudad(id):
            return None

        buscar_ciudad(7)  # 'desconocido'
    """

    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            resultado_funcion = func(*args, **kwargs) 
            if resultado_funcion is None:
                return reemplazo
            return resultado_funcion

        return envoltorio

    return decorador


# ---------------------------------------------------------------------------
# 5. Apilar decoradores — el orden importa
# ---------------------------------------------------------------------------
# Estos dos ya están hechos. Usalos, no los toques.
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


# Agregale a CADA UNA los dos decoradores de arriba, apilados en el orden que
# haga que el resultado sea el que dice el nombre. No cambies el cuerpo.
@duplicar
@sumar_uno
def duplica_despues_de_sumar(n: int) -> int:
    """Con n=5 tiene que dar 12:  (5 + 1) * 2"""
    return n


@sumar_uno
@duplicar
def suma_despues_de_duplicar(n: int) -> int:
    """Con n=5 tiene que dar 11:  (5 * 2) + 1"""
    return n


# ---------------------------------------------------------------------------
# 6. Un decorador que NO envuelve: el registro
# ---------------------------------------------------------------------------
TAREAS: dict = {}


def registrar(func):
    """Decorador: anota `func` en el dict TAREAS bajo su propio nombre y la
    devuelve INTACTA.

    No hay envoltorio acá: la función decorada tiene que seguir siendo el mismo
    objeto que se definió (hay un test con `is`). Por eso tampoco hace falta
    `wraps`.

    Pista: el nombre de una función está en `func.__name__` (sección 6 de la
    lección 04).

    Después de importar este módulo:
        TAREAS  # {'limpiar_temporales': <function ...>, 'enviar_reporte': ...}
    """

    TAREAS[func.__name__] = func
    return func


# Estas dos ya están decoradas: son las que van a aparecer en TAREAS.
@registrar
def limpiar_temporales() -> str:
    return "temporales limpiados"


@registrar
def enviar_reporte(destino: str) -> str:
    return f"reporte enviado a {destino}"


# ---------------------------------------------------------------------------
# 7. Caché a mano
# ---------------------------------------------------------------------------
def memorizar(func):
    """Decorador: guarda los resultados ya calculados y no vuelve a ejecutar el
    cuerpo de `func` para los mismos argumentos.

    Alcanza con soportar argumentos POSICIONALES: la clave del caché es la
    tupla `args` (por eso el envoltorio recibe una tupla, ya viene lista para
    usar como clave de dict).

    Acordate del closure de la lección 04: el dict del caché se crea UNA vez,
    afuera del envoltorio.

    Hay un test que verifica que el cuerpo se ejecute una sola vez por
    argumento distinto.
    """
    resultados = {}

    @wraps(func)
    def envoltorio(*args):
        if args not in resultados:
            resultados[args] = func(*args)
        return resultados[args]

    return envoltorio


# ---------------------------------------------------------------------------
# 8. Lo mismo, pero con functools
# ---------------------------------------------------------------------------
# Agregale el decorador de la biblioteca estándar que hace lo del ejercicio 7.
# Una línea. No toques el cuerpo.
@cache
def fib(n: int) -> int:
    """Fibonacci recursivo.

    Sin caché, fib(35) hace unos 30 millones de llamadas y tarda segundos.
    Con caché, es instantáneo. Hay un test que lo cronometra.

    >>> fib(10)
    55
    """
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# ---------------------------------------------------------------------------
# 9. El decorador clásico: cronometrar
# ---------------------------------------------------------------------------
def cronometrar(func):
    """Decorador: mide cuánto tardó la llamada y lo deja en el atributo
    `.ultima_duracion` del envoltorio (en segundos).

    Devolvé el resultado de `func`, no la duración.

    Para medir usá `time.perf_counter()`, que devuelve un float de segundos.
    Es el reloj que hay que usar para medir intervalos: `time.time()` puede
    saltar para atrás si el sistema ajusta la hora.

    Acordate de importar `time` arriba de todo.

    Uso:
        @cronometrar
        def trabajar():
            return "listo"

        trabajar()  # 'listo'
        trabajar.ultima_duracion  # 3.4e-06
    """

    @wraps(func)
    def envoltorio(*args, **kwargs):
        primer_medicion = perf_counter()
        resultado_funcion = func(*args, **kwargs)
        envoltorio.ultima_duracion = perf_counter() - primer_medicion  # type: ignore[attr-defined]
        return resultado_funcion

    envoltorio.ultima_duracion = 0.0  # type: ignore[attr-defined]
    return envoltorio


# ---------------------------------------------------------------------------
# 10. El decorador que se come al ejercicio 1
# ---------------------------------------------------------------------------
def aplicar_a_resultado(transformacion):
    """Fábrica de decoradores: aplica `transformacion` (una función) al
    resultado de `func`.

    Es la versión genérica del ejercicio 1: `sin_espacios` no es más que
    `aplicar_a_resultado(str.strip)`. Hay un test que lo comprueba.

    Uso:
        @aplicar_a_resultado(str.upper)
        def leer():
            return "hola"

        leer()  # 'HOLA'
    """

    def decorador(func):
        @wraps(func)
        def envoltorio(*args, **kwargs):
            return transformacion(func(*args, **kwargs))

        return envoltorio

    return decorador

if __name__ == "__main__":
    # Un lugar para probar cosas a mano mientras resolvés.
    print(TAREAS)
    @aplicar_a_resultado(str.upper)
    def leer():
        return "hola"

    print(leer())  # 'HOLA'
