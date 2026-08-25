"""
Lección 04 — Solución de referencia.

LEÉ ESTO SOLO DESPUÉS de tener tus 46 tests en verde.
"""

import operator
from collections.abc import Callable
from functools import partial


def promedio(*numeros: float) -> float:
    # La guarda va ANTES de dividir. Si la ponés después, `len(numeros)` es 0
    # y explota con ZeroDivisionError antes de llegar al if.
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)


def describir(**atributos) -> str:
    # `sorted(atributos)` sobre un dict itera sus CLAVES ordenadas.
    # Lo de adentro del join es una generator expression: una comprehension
    # sin corchetes. No arma la lista intermedia, va produciendo de a uno.
    return "; ".join(f"{clave}={atributos[clave]}" for clave in sorted(atributos))


def crear_url(base: str, **params) -> str:
    if not params:
        return base
    # Nombrar el paso intermedio evita mezclar f-string con concatenación.
    query = "&".join(f"{clave}={params[clave]}" for clave in sorted(params))
    return f"{base}?{query}"


def crear_usuario(nombre: str, *, admin: bool = False, activo: bool = True) -> dict:
    # El `*` pelado es todo el ejercicio: obliga a `crear_usuario("ana", admin=True)`.
    # El dict va como literal, no como `dict(nombre=nombre, ...)`: es la forma
    # canónica y la que pide ruff (regla C408).
    return {"nombre": nombre, "admin": admin, "activo": activo}


def llamar_con(func: Callable, argumentos: list, nombrados: dict):
    # El * y el ** del lado de la LLAMADA: reparten en vez de recoger.
    return func(*argumentos, **nombrados)


def aplicar_a_todos(func: Callable, items: list) -> list:
    return [func(item) for item in items]


# `operator` tiene los operadores de Python empaquetados como funciones.
# Existe justo para esto: evita escribir `lambda a, b: a + b`.
OPERACIONES: dict[str, Callable] = {
    "sumar": operator.add,
    "restar": operator.sub,
    "multiplicar": operator.mul,
    "maximo": max,
}


def calcular(operacion: str, a: float, b: float) -> float | None:
    # `None` acá es centinela: `is None`, no truthiness. Una operación que
    # devolviera 0 no tendría por qué confundirse con "no existe".
    funcion = OPERACIONES.get(operacion)
    if funcion is None:
        return None
    return funcion(a, b)


def hacer_multiplicador(factor: float) -> Callable[[float], float]:
    def multiplicar(numero: float) -> float:
        return numero * factor  # `factor` viene del closure

    return multiplicar  # sin paréntesis: devuelvo la función


def hacer_validador(minimo: float, maximo: float) -> Callable[[float], bool]:
    # Una función que devuelve bool se nombra como pregunta: `esta_en_rango`,
    # no `numero_valido` (eso suena a variable que guarda un bool).
    def esta_en_rango(numero: float) -> bool:
        return minimo <= numero <= maximo

    return esta_en_rango


def contar_llamadas(func: Callable) -> Callable:
    # Esto YA es un decorador. En la lección 05 lo único que cambia es que en
    # vez de `f = contar_llamadas(f)` vas a escribir `@contar_llamadas`.
    def envoltorio(*args, **kwargs):
        # Se cuenta ANTES de llamar: si `func` revienta, la llamada igual
        # quedó contada. Contarla después significaría "llamadas exitosas".
        # Las dos son válidas; lo que no vale es no haberlo decidido.
        envoltorio.llamadas += 1
        return func(*args, **kwargs)

    # `.llamadas` cuelga del envoltorio, no de `func`: la función original
    # queda intacta. `+=` sobre un atributo no necesita `nonlocal`, porque no
    # reasigna el nombre `envoltorio`, muta el objeto.
    envoltorio.llamadas = 0
    return envoltorio


def hacer_redondeador(decimales: int) -> Callable[[float], float]:
    # `ndigits` es el SEGUNDO parámetro de round, así que se congela por
    # nombre. `partial(round, decimales)` congelaría el primero: mal.
    return partial(round, ndigits=decimales)


def ordenador_por(*claves: str) -> Callable[[list[dict]], list[dict]]:
    def ordenar(registros: list[dict]) -> list[dict]:
        # La clave de ordenamiento es la tupla de valores de esas claves.
        # `tuple(...)` es el constructor, igual que `list(...)` o `set(...)`;
        # lo de adentro es una generator expression.
        #
        # No hay "tuple comprehension": `(x for x in y)` es un generador, no
        # una tupla. Por eso hace falta envolverlo en `tuple(...)`.
        #
        # Detalle: una LISTA también sirve como clave, porque las listas se
        # comparan elemento por elemento igual que las tuplas:
        #     key=lambda r: [r[clave] for clave in claves]
        # La tupla es la convención (inmutable y hashable), pero las dos andan.
        return sorted(registros, key=lambda r: tuple(r[clave] for clave in claves))

    return ordenar


if __name__ == "__main__":
    # Las dos funciones de la lección 03, ahora fabricadas:
    ordenar_por_edad = ordenador_por("edad")
    ordenar_catalogo = ordenador_por("categoria", "precio")

    print(ordenar_por_edad([{"edad": 30}, {"edad": 25}]))
    print(calcular("maximo", 3, 9))
    print(describir(peso=3, color="rojo"))
