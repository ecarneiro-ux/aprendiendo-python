"""
Lección 02 — Solución de referencia.

LEÉ ESTO SOLO DESPUÉS de tener tus 28 tests en verde.
"""


# ---------------------------------------------------------------------------
# 1. Comprehension básica
# ---------------------------------------------------------------------------
def cuadrados(n: int) -> list[int]:
    # Ojo con reusar `n` como variable del for: pisa el parámetro.
    # Acá funcionaría igual (el range() del for más externo se evalúa afuera),
    # pero en cuanto anidás comprehensions deja de funcionar. Usá otro nombre.
    return [x**2 for x in range(n)]


# ---------------------------------------------------------------------------
# 2. Filtro
# ---------------------------------------------------------------------------
def solo_pares(numeros: list[int]) -> list[int]:
    return [n for n in numeros if n % 2 == 0]


# ---------------------------------------------------------------------------
# 3. Filtrar y transformar
# ---------------------------------------------------------------------------
def normalizar(nombres: list[str]) -> list[str]:
    # `if n.strip()` usa truthiness: el string vacío ya es falso.
    # No hace falta `!= ""`.
    return [n.strip().title() for n in nombres if n.strip()]


# ---------------------------------------------------------------------------
# 4. enumerate
# ---------------------------------------------------------------------------
def posiciones(items: list[str]) -> dict[str, int]:
    # Si una clave se repite, la última asignación pisa a la anterior.
    # Por eso "gana el último índice" sale solo, sin escribir nada extra.
    return {item: i for i, item in enumerate(items)}


# ---------------------------------------------------------------------------
# 5. zip
# ---------------------------------------------------------------------------
def combinar(claves: list[str], valores: list[int]) -> dict[str, int]:
    # dict() acepta directamente pares (clave, valor), que es justo lo que
    # produce zip(). No hace falta comprehension.
    return dict(zip(claves, valores))


# ---------------------------------------------------------------------------
# 6. set comprehension
# ---------------------------------------------------------------------------
def palabras_unicas(texto: str) -> set[str]:
    # Una sola pasada, sin lista intermedia.
    # Si te encontrás escribiendo `{x for x in coleccion}` sin transformar ni
    # filtrar, lo que querías era `set(coleccion)`.
    return {p.lower() for p in texto.split()}


# ---------------------------------------------------------------------------
# 7. Operaciones de conjuntos
# ---------------------------------------------------------------------------
def elementos_comunes(a: list, b: list) -> set:
    # `&` es intersección. También existe a.intersection(b), más explícito
    # cuando el operador no se entiende de un vistazo.
    return set(a) & set(b)


# ---------------------------------------------------------------------------
# 8. set comprehension con filtro
# ---------------------------------------------------------------------------
def repetidos(items: list) -> set:
    # OJO con el costo: .count() recorre la lista entera por CADA elemento.
    # Esto es O(n²) — el mismo problema que `in` sobre una lista.
    # En la lección 03 lo reescribimos con Counter, que lo hace en O(n):
    #
    #     from collections import Counter
    #     return {x for x, veces in Counter(items).items() if veces > 1}
    return {x for x in items if items.count(x) > 1}


# ---------------------------------------------------------------------------
# 9. Comprehension anidada
# ---------------------------------------------------------------------------
def aplanar(matriz: list[list]) -> list:
    # Los `for` van en el MISMO orden que si los escribieras anidados:
    #     for fila in matriz:
    #         for n in fila:
    # Es la parte menos intuitiva de la sintaxis. Casi todo el mundo la
    # escribe al revés la primera vez.
    return [n for fila in matriz for n in fila]


# ---------------------------------------------------------------------------
# 10. dict comprehension sobre .items()
# ---------------------------------------------------------------------------
def con_stock(inventario: dict[str, int]) -> dict[str, int]:
    return {producto: cant for producto, cant in inventario.items() if cant > 0}


# ---------------------------------------------------------------------------
# 11. El caso donde el bucle es la herramienta correcta
# ---------------------------------------------------------------------------
def agrupar_por_inicial(nombres: list[str]) -> dict[str, list[str]]:
    # Una comprehension construye cada elemento de forma independiente.
    # Acá cada clave ACUMULA: hay que leer lo que ya había y agregarle.
    # Ese estado que se arrastra entre vueltas es lo que pide un bucle.
    agrupados: dict[str, list[str]] = {}
    for nombre in nombres:
        # .upper() dice "esta letra en mayúscula".
        # .title() dice "inicial de cada palabra en mayúscula" — sobre un solo
        # carácter da igual, pero conviene usar el método que expresa la intención.
        inicial = nombre[0].upper()
        # setdefault devuelve la lista de esa clave, creándola vacía si no existía.
        agrupados.setdefault(inicial, []).append(nombre)
    return agrupados
    # En la lección 03: defaultdict(list) hace innecesario el setdefault.


# ---------------------------------------------------------------------------
# Probar el archivo a mano, sin que se ejecute al importarlo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Este bloque corre SOLO con `python solucion_comentada.py`.
    # Al importarlo (como hace pytest), __name__ vale el nombre del módulo
    # y nada de esto se ejecuta.
    print(agrupar_por_inicial(["Ana", "Luis", "Alba"]))
    print(normalizar(["  ana perez ", "", "LUIS GOMEZ"]))
