"""
Lección 03 — Ordenar, lambdas y collections.

Completá cada función reemplazando el `...` por tu código.
Corré los tests con:  pytest leccion-03 -v

Los ejercicios 8 y 9 son reescrituras de lo que ya hiciste en las lecciones
01 y 02. Fijate cuánto código desaparece.
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# 1. key= con una función que ya existe
# ---------------------------------------------------------------------------
def ordenar_por_largo(palabras: list[str]) -> list[str]:
    """Ordena las palabras de más corta a más larga.

    No pases una lambda: existe una función que hace justo esto.
    Las que empatan en largo mantienen el orden original (el sort es estable).

    >>> ordenar_por_largo(["python", "es", "genial"])
    ['es', 'python', 'genial']
    """
    return sorted(palabras, key=len)


# ---------------------------------------------------------------------------
# 2. reverse=
# ---------------------------------------------------------------------------
def ordenar_desc(numeros: list[int]) -> list[int]:
    """Ordena de mayor a menor SIN modificar la lista original.

    >>> ordenar_desc([3, 1, 2])
    [3, 2, 1]
    """
    return sorted(numeros, reverse=True)


# ---------------------------------------------------------------------------
# 3. max con key=
# ---------------------------------------------------------------------------
def mas_larga(palabras: list[str]) -> str | None:
    """Devuelve la palabra más larga. Si hay empate, la primera.

    Con una lista vacía devolvé None (no hagas un if: `max` tiene un
    parámetro para esto).

    >>> mas_larga(["hola", "buenas", "chau"])
    'buenas'
    """
    return max(palabras, key=len, default=None)


# ---------------------------------------------------------------------------
# 4. lambda sobre una lista de dicts
# ---------------------------------------------------------------------------
def ordenar_por_edad(personas: list[dict]) -> list[dict]:
    """Ordena las personas de menor a mayor edad.

    Cada persona es un dict con las claves "nombre" y "edad".

    >>> ordenar_por_edad([{"nombre": "Ana", "edad": 30},
    ...                   {"nombre": "Luis", "edad": 25}])
    [{'nombre': 'Luis', 'edad': 25}, {'nombre': 'Ana', 'edad': 30}]
    """
    return sorted(personas, key=lambda p: p["edad"])


# ---------------------------------------------------------------------------
# 5. Clave-tupla: dos criterios, misma dirección
# ---------------------------------------------------------------------------
def ordenar_catalogo(productos: list[dict]) -> list[dict]:
    """Ordena por categoría alfabéticamente y, dentro de cada una, por precio
    de menor a mayor.

    Cada producto es un dict con "nombre", "categoria" y "precio".
    Resolvelo con UNA sola llamada a sorted().
    """
    return sorted(productos, key=lambda p: (p["categoria"], p["precio"]))


# ---------------------------------------------------------------------------
# 6. Clave-tupla: criterios en direcciones OPUESTAS
# ---------------------------------------------------------------------------
def ranking(votos: dict[str, int]) -> list[str]:
    """Devuelve los candidatos ordenados por votos de mayor a menor.
    Si dos empatan en votos, van en orden alfabético ascendente.

    Devolvé solo los nombres, no los votos.

    Ojo: `reverse=True` te invierte los DOS criterios. Releé la sección 5.

    >>> ranking({"ana": 5, "luis": 8, "zoe": 5})
    ['luis', 'ana', 'zoe']
    """
    resultado = sorted(votos.items(), key=lambda item: (-item[1], item[0]))
    return [c[0] for c in resultado]


# ---------------------------------------------------------------------------
# 7. Counter.most_common
# ---------------------------------------------------------------------------
def top_palabras(texto: str, n: int) -> list[tuple[str, int]]:
    """Devuelve las n palabras más frecuentes con su cantidad, de mayor a menor.

    Ignorá mayúsculas/minúsculas.

    >>> top_palabras("el gato y el perro y el pez", 2)
    [('el', 3), ('y', 2)]
    """
    texto_nor = Counter(texto.lower().split())
    return texto_nor.most_common(n)


# ---------------------------------------------------------------------------
# 8. REESCRITURA — el `repetidos` de la lección 02, ahora en O(n)
# ---------------------------------------------------------------------------
def repetidos(items: list) -> set:
    """Devuelve el conjunto de elementos que aparecen más de una vez.

    Tu versión de la lección 02 usaba `.count()` dentro de una comprehension:
    O(n²). Esta tiene que recorrer la lista UNA sola vez.

    Prohibido usar `.count()`.

    >>> repetidos([1, 2, 2, 3, 3, 3]) == {2, 3}
    True
    """
    return {c for c, x in Counter(items).items() if x > 1}


# ---------------------------------------------------------------------------
# 9. REESCRITURA — el `agrupar_por_inicial` de la lección 02, con defaultdict
# ---------------------------------------------------------------------------
def agrupar_por_inicial(nombres: list[str]) -> dict[str, list[str]]:
    """Agrupa los nombres por su letra inicial en mayúscula.

    Mismo resultado que en la lección 02, pero con `defaultdict` en vez de
    `setdefault`. Devolvé un dict común (convertilo con `dict(...)`).

    >>> agrupar_por_inicial(["Ana", "Luis", "Alba"])
    {'A': ['Ana', 'Alba'], 'L': ['Luis']}
    """
    agrupados = defaultdict(list)
    for n in nombres:
        agrupados[n[0].upper()].append(n)
    return dict(agrupados)


# ---------------------------------------------------------------------------
# 10. Combinar dicts
# ---------------------------------------------------------------------------
def fusionar_config(default: dict, usuario: dict) -> dict:
    """Aplica la config del usuario sobre la config por defecto.

    En los conflictos gana el usuario. NINGUNO de los dos dicts que recibís
    puede quedar modificado.

    >>> fusionar_config({"host": "localhost", "puerto": 8000}, {"puerto": 9000})
    {'host': 'localhost', 'puerto': 9000}
    """
    return default | usuario


# ---------------------------------------------------------------------------
# 11. Desempaquetado con *
# ---------------------------------------------------------------------------
def separar_cabecera(filas: list[list]) -> tuple[list, list[list]]:
    """Separa la primera fila (la cabecera de un CSV) del resto.

    Devolvé una tupla (cabecera, resto).
    Si `filas` está vacía, devolvé ([], []).

    >>> separar_cabecera([["id", "nombre"], [1, "Ana"], [2, "Luis"]])
    (['id', 'nombre'], [[1, 'Ana'], [2, 'Luis']])
    """
    if filas == []:
        return [], []
    else:
        fila, *resto = filas
        return fila, resto


if __name__ == "__main__":
    print(agrupar_por_inicial(["Ana", "Ana", "Ana"]))
