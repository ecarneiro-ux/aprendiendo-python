"""
Lección 03 — Solución de referencia.

LEÉ ESTO SOLO DESPUÉS de tener tus 27 tests en verde.
"""

from collections import Counter, defaultdict


def ordenar_por_largo(palabras: list[str]) -> list[str]:
    return sorted(palabras, key=len)


def ordenar_desc(numeros: list[int]) -> list[int]:
    return sorted(numeros, reverse=True)


def mas_larga(palabras: list[str]) -> str | None:
    # `default=` evita el ValueError con lista vacía sin necesidad de un if.
    return max(palabras, key=len, default=None)


def ordenar_por_edad(personas: list[dict]) -> list[dict]:
    return sorted(personas, key=lambda p: p["edad"])


def ordenar_catalogo(productos: list[dict]) -> list[dict]:
    return sorted(productos, key=lambda p: (p["categoria"], p["precio"]))


def ranking(votos: dict[str, int]) -> list[str]:
    # `.items()` da pares (nombre, votos). El `-` invierte SOLO ese criterio,
    # dejando el alfabético ascendente.
    ordenados = sorted(votos.items(), key=lambda item: (-item[1], item[0]))
    # Desempaquetar en el for es más claro que indexar con [0]:
    # se lee "de cada par, quedate con el nombre y descartá los votos".
    # El guión bajo es la convención para "esto no lo voy a usar".
    return [nombre for nombre, _ in ordenados]


def top_palabras(texto: str, n: int) -> list[tuple[str, int]]:
    return Counter(texto.lower().split()).most_common(n)


def repetidos(items: list) -> set:
    # Counter recorre la lista UNA vez: O(n).
    # La versión de la lección 02 con .count() era O(n²).
    return {elemento for elemento, veces in Counter(items).items() if veces > 1}


def agrupar_por_inicial(nombres: list[str]) -> dict[str, list[str]]:
    agrupados = defaultdict(list)
    for nombre in nombres:
        agrupados[nombre[0].upper()].append(nombre)
    # dict(...) para que el que lo reciba no invente claves al consultarlas.
    return dict(agrupados)


def fusionar_config(default: dict, usuario: dict) -> dict:
    # `|` devuelve un dict NUEVO; gana el de la derecha. Ninguno se modifica.
    # Ojo con `default.update(usuario)`: eso SÍ modifica `default`.
    return default | usuario


def separar_cabecera(filas: list[list]) -> tuple[list, list[list]]:
    # `if not filas` en vez de `if filas == []`: una lista vacía ya es falsa,
    # y así funciona igual con cualquier iterable, no solo con listas.
    if not filas:
        return [], []
    # Sin `else`: si entraste al if, ya te fuiste con el return.
    cabecera, *resto = filas
    return cabecera, resto


if __name__ == "__main__":
    print(ranking({"ana": 5, "luis": 8, "zoe": 5}))
    print(separar_cabecera([["id", "nombre"], [1, "Ana"]]))
