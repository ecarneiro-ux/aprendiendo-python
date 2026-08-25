"""
Lección 04 — Funciones flexibles, funciones como valores, closures.

Completá cada función reemplazando el `...` por tu código.
Corré los tests con:  pytest leccion-04 -v

Antes de arrancar:  python leccion-04/demo_closures.py

El ejercicio 10 es el puente a los decoradores (lección 05).
El 12 es una reescritura: reemplaza DOS funciones de la lección 03.
"""

from collections.abc import Callable
from functools import partial

# ---------------------------------------------------------------------------
# 1. *args
# ---------------------------------------------------------------------------
def promedio(*numeros: float) -> float:
    """Devuelve el promedio de los números que reciba.

    Se llama con argumentos sueltos: promedio(1, 2, 3), NO con una lista.
    Sin argumentos devolvé 0.0 — y acordate de dónde va esa guarda.

    >>> promedio(1, 2, 3)
    2.0
    >>> promedio()
    0.0
    """
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)


# ---------------------------------------------------------------------------
# 2. **kwargs
# ---------------------------------------------------------------------------
def describir(**atributos)-> str:   
    """Arma un texto "clave=valor" con todo lo que reciba, separado por "; ".

    Las claves van en orden alfabético (no en el orden en que las pasaron).
    Sin atributos devolvé "".

    >>> describir(peso=3, color="rojo")
    'color=rojo; peso=3'
    >>> describir()
    ''
    """
    return "; ".join(f"{clave}={atributos[clave]}" for clave in sorted(atributos))


# ---------------------------------------------------------------------------
# 3. **kwargs con algo de trabajo
# ---------------------------------------------------------------------------
def crear_url(base: str, **params) -> str:
    """Pega los parámetros a la URL como query string.

    Formato: base + "?" + "clave=valor" unidos por "&", claves en orden
    alfabético. Si no hay parámetros, devolvé la base tal cual (sin "?").

    >>> crear_url("https://api.com/datos", pagina=2, orden="asc")
    'https://api.com/datos?orden=asc&pagina=2'
    >>> crear_url("https://api.com/datos")
    'https://api.com/datos'
    """
    if not params:
        return base
    return f"{base}?" + "&".join(f"{param}={params[param]}" for param in sorted(params))


# ---------------------------------------------------------------------------
# 4. Parámetros keyword-only
# ---------------------------------------------------------------------------
def crear_usuario(nombre: str, *, admin: bool = False, activo: bool = True) -> dict:
    """Devuelve {"nombre": ..., "admin": ..., "activo": ...}.

    ⚠️ Tenés que MODIFICAR LA FIRMA: `admin` y `activo` tienen que ser
    keyword-only, para que `crear_usuario("ana", True)` sea un TypeError y
    haya que escribir `crear_usuario("ana", admin=True)`.

    Hay un test que verifica justamente que la llamada posicional falle.

    >>> crear_usuario("ana", admin=True)
    {'nombre': 'ana', 'admin': True, 'activo': True}
    """
    return {
        "nombre": nombre,
        "admin": admin,
        "activo": activo,
    }  # Antes de ruff dict(nombre=nombre, admin=admin, activo=activo)


# ---------------------------------------------------------------------------
# 5. El * y el ** del lado de la LLAMADA
# ---------------------------------------------------------------------------
def llamar_con(func: Callable, argumentos: list, nombrados: dict):
    """Llama a `func` repartiendo la lista como argumentos posicionales y el
    dict como argumentos por nombre. Devolvé lo que devuelva `func`.

    Una sola línea. No uses ifs.

    >>> llamar_con(max, [3, 9, 1], {})
    9
    >>> llamar_con(round, [3.14159], {"ndigits": 2})
    3.14
    """
    return func(*argumentos, **nombrados)


# ---------------------------------------------------------------------------
# 6. Una función como parámetro
# ---------------------------------------------------------------------------
def aplicar_a_todos(func: Callable, items: list) -> list:
    """Devuelve una lista nueva con `func` aplicada a cada elemento.

    Sin bucles con .append(): esto es una comprehension.

    >>> aplicar_a_todos(len, ["hola", "chau"])
    [4, 4]
    """
    return [func(item) for item in items]


# ---------------------------------------------------------------------------
# 7. Dispatch table (el reemplazo del switch)
# ---------------------------------------------------------------------------
OPERACIONES: dict[str, Callable] = {
    "sumar": lambda a, b: a + b,
    "restar": lambda a, b: a - b,
    "multiplicar": lambda a, b: a * b,
    "maximo": max,
}


def calcular(operacion: str, a: float, b: float) -> float | None:
    """Aplica la operación pedida sobre `a` y `b`.

    Operaciones: "sumar", "restar", "multiplicar", "maximo".
    Si la operación no existe, devolvé None.

    ⚠️ Prohibido el if/ encadenado. Completá el dict OPERACIONES de arriba
    (a nivel módulo, no adentro de la función) y buscá ahí.

    >>> calcular("sumar", 2, 3)
    5
    >>> calcular("potencia", 2, 3) is None
    True
    """
    funcion = OPERACIONES.get(operacion)
    if funcion is None:
        return None
    return funcion(a,b)


# ---------------------------------------------------------------------------
# 8. Closure simple
# ---------------------------------------------------------------------------
def hacer_multiplicador(factor: float) -> Callable[[float], float]:
    """Devuelve una FUNCIÓN que multiplica lo que reciba por `factor`.

    Ojo: devolvés la función, no el resultado. Sin paréntesis en el return.

    >>> doble = hacer_multiplicador(2)
    >>> doble(5)
    10
    """

    def multiplicar(numero: float):
        return factor * numero

    return multiplicar


# ---------------------------------------------------------------------------
# 9. Closure que captura dos valores
# ---------------------------------------------------------------------------
def hacer_validador(minimo: float, maximo: float) -> Callable[[float], bool]:
    """Devuelve una función que dice si un número está entre `minimo` y
    `maximo`, ambos incluidos.

    >>> es_edad_valida = hacer_validador(0, 120)
    >>> es_edad_valida(30), es_edad_valida(150)
    (True, False)
    """

    def numero_valido(numero: float):
        return minimo <= numero <= maximo

    return numero_valido


# ---------------------------------------------------------------------------
# 10. Closure con estado + *args/**kwargs   ← el puente a la lección 05
# ---------------------------------------------------------------------------
def contar_llamadas(func: Callable) -> Callable:
    """Devuelve una función que hace lo mismo que `func` pero además lleva la
    cuenta de cuántas veces se la llamó.

    Requisitos:
      - el envoltorio acepta CUALQUIER combinación de argumentos y se los pasa
        tal cual a `func`
      - devuelve lo mismo que devolvería `func`
      - expone la cuenta en el atributo `.llamadas` del envoltorio, que
        arranca en 0

    Pista: la sección 6 (una función es un objeto, y le podés colgar atributos)
    te alcanza para resolverlo. Si en vez de eso llevás la cuenta en una
    variable del closure, ahí sí vas a necesitar `nonlocal`.

    >>> saludar_contado = contar_llamadas(str.upper)
    >>> saludar_contado.llamadas
    0
    >>> saludar_contado("hola")
    'HOLA'
    >>> saludar_contado.llamadas
    1
    """

    def envoltorio(*args, **kwargs):
        envoltorio.llamadas += 1
        return func(*args, **kwargs)

    envoltorio.llamadas = 0
    return envoltorio


# ---------------------------------------------------------------------------
# 11. functools.partial
# ---------------------------------------------------------------------------



def hacer_redondeador(decimales: int) -> Callable[[float], float]:
    """Devuelve una función que redondea a `decimales` decimales.

    Esto se puede hacer con un closure, pero acá la función que querés
    especializar ya existe (`round`). Resolvelo con `partial`, en una línea.

    Pista: `round(numero, ndigits)`. Fijate CUÁL de los dos parámetros estás
    congelando y releé la sección 8.

    >>> a_centavos = hacer_redondeador(2)
    >>> a_centavos(3.14159)
    3.14
    """
    return partial(round, ndigits=decimales)


# ---------------------------------------------------------------------------
# 12. REESCRITURA — `ordenar_por_edad` + `ordenar_catalogo` de la lección 03
# ---------------------------------------------------------------------------
def ordenador_por(*claves: str)-> Callable[[list[dict]], list[dict]]:  
    """Devuelve una función que ordena una lista de dicts por esas claves.

    En la lección 03 escribiste dos funciones casi idénticas: una ordenaba por
    "edad" y la otra por ("categoria", "precio"). Las dos salen de acá:

        ordenar_por_edad = ordenador_por("edad")
        ordenar_catalogo = ordenador_por("categoria", "precio")

    La lista original no se toca (sorted, no .sort()).

    Pista: la clave de ordenamiento de cada dict es la tupla de sus valores
    para esas claves, en orden. Armala con una comprehension.

    >>> por_edad = ordenador_por("edad")
    >>> por_edad([{"edad": 30}, {"edad": 25}])
    [{'edad': 25}, {'edad': 30}]
    """

    def ordenar(lista: list[dict]):
        return sorted(lista, key=lambda item: tuple(item[clave] for clave in claves))

    return ordenar


if __name__ == "__main__":
    # Un lugar para probar cosas a mano mientras resolvés.
    print("PRUEBAS")
