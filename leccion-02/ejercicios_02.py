"""
Lección 02 — Estructuras de datos y comprehensions.

Completá cada función reemplazando el `...` por tu código.
Corré los tests con:  pytest leccion-02 -v

REGLA DE ESTA LECCIÓN: nada de `lista = []` + `for` + `.append()`.
Salvo en el ejercicio 11, donde está justificado y te explico por qué.
"""


# ---------------------------------------------------------------------------
# 1. Tu primera comprehension
# ---------------------------------------------------------------------------
def cuadrados(n: int) -> list[int]:
    """Devuelve los cuadrados de 0 a n-1.

    >>> cuadrados(5)
    [0, 1, 4, 9, 16]
    """
    return [x**2 for x in range(n)]


# ---------------------------------------------------------------------------
# 2. Comprehension con filtro
# ---------------------------------------------------------------------------
def solo_pares(numeros: list[int]) -> list[int]:
    """Devuelve solo los números pares, en el mismo orden.

    >>> solo_pares([1, 2, 3, 4, 5, 6])
    [2, 4, 6]
    """
    return [n for n in numeros if n % 2 == 0]


# ---------------------------------------------------------------------------
# 3. Filtrar Y transformar en una sola pasada
# ---------------------------------------------------------------------------
def normalizar(nombres: list[str]) -> list[str]:
    """Limpia una lista de nombres que vino sucia de un formulario.

    - Saca los espacios de los extremos (buscá `.strip()`)
    - Deja cada palabra con la inicial en mayúscula (buscá `.title()`)
    - Descarta los que quedan vacíos

    >>> normalizar(["  ana perez ", "", "LUIS GOMEZ", "   "])
    ['Ana Perez', 'Luis Gomez']
    """
    return [n.strip().title() for n in nombres if n.strip()]


# ---------------------------------------------------------------------------
# 4. enumerate
# ---------------------------------------------------------------------------
def posiciones(items: list[str]) -> dict[str, int]:
    """Devuelve un dict que mapea cada elemento a su índice.

    Si un elemento se repite, gana el ÚLTIMO índice (te va a salir solo).

    >>> posiciones(["a", "b", "c"])
    {'a': 0, 'b': 1, 'c': 2}
    """
    return {item: idx for idx, item in enumerate(items)}


# ---------------------------------------------------------------------------
# 5. zip
# ---------------------------------------------------------------------------
def combinar(claves: list[str], valores: list[int]) -> dict[str, int]:
    """Arma un dict emparejando ambas listas posición a posición.

    Si tienen distinto largo, cortá con la más corta (zip lo hace solo).
    Se puede resolver en UNA línea, sin comprehension.

    >>> combinar(["a", "b"], [1, 2])
    {'a': 1, 'b': 2}
    """
    return dict(zip(claves, valores))


# ---------------------------------------------------------------------------
# 6. set
# ---------------------------------------------------------------------------
def palabras_unicas(texto: str) -> set[str]:
    """Devuelve el conjunto de palabras distintas, en minúscula.

    >>> palabras_unicas("El gato y el Gato")
    {'el', 'gato', 'y'}
    """
    return set(texto.lower().split())


# ---------------------------------------------------------------------------
# 7. Operaciones de conjuntos
# ---------------------------------------------------------------------------
def elementos_comunes(a: list, b: list) -> set:
    """Devuelve los elementos que aparecen en AMBAS listas.

    Usá una operación de conjuntos, no un bucle con `in`.

    >>> elementos_comunes([1, 2, 3], [2, 3, 4]) == {2, 3}
    True
    """
    return set(a) & set(b)


# ---------------------------------------------------------------------------
# 8. set comprehension
# ---------------------------------------------------------------------------
def repetidos(items: list) -> set:
    """Devuelve el conjunto de elementos que aparecen MÁS DE UNA VEZ.

    Pista: las listas tienen un método `.count(x)`.

    >>> repetidos([1, 2, 2, 3, 3, 3]) == {2, 3}
    True
    """
    return {n for n in items if items.count(n)>1}


# ---------------------------------------------------------------------------
# 9. Comprehension anidada
# ---------------------------------------------------------------------------
def aplanar(matriz: list[list]) -> list:
    """Convierte una lista de listas en una lista simple.

    >>> aplanar([[1, 2], [3, 4], [5]])
    [1, 2, 3, 4, 5]
    """
    return [n for fila in matriz for n in fila]


# ---------------------------------------------------------------------------
# 10. dict comprehension sobre .items()
# ---------------------------------------------------------------------------
def con_stock(inventario: dict[str, int]) -> dict[str, int]:
    """Devuelve solo los productos con stock mayor a 0.

    >>> con_stock({"pan": 3, "leche": 0, "queso": 7})
    {'pan': 3, 'queso': 7}
    """
    return {k: v for k, v in inventario.items() if v > 0}


# ---------------------------------------------------------------------------
# 11. LA EXCEPCIÓN — acá el bucle con .append() SÍ va
# ---------------------------------------------------------------------------
def agrupar_por_inicial(nombres: list[str]) -> dict[str, list[str]]: 
    """Agrupa los nombres por su letra inicial (en mayúscula).

    Esto NO se puede hacer con una comprehension simple, porque cada clave
    acumula varios elementos: necesitás leer lo que ya había y agregarle.
    Ese es exactamente el caso donde el bucle es la herramienta correcta.

    Pista: `dict.setdefault(clave, [])` devuelve la lista de esa clave,
    creándola vacía si no existía. Sobre eso podés hacer `.append()`.

    Los nombres vienen en el orden en que aparecen.

    >>> agrupar_por_inicial(["Ana", "Luis", "Alba"])
    {'A': ['Ana', 'Alba'], 'L': ['Luis']}
    """
    agrupados = {}
    for n in nombres:
        inicial = n[0].upper()
        agrupados.setdefault(inicial, []).append(n)
    return agrupados



if __name__ == "__main__":
    print(normalizar(["  ana perez ", "", "LUIS GOMEZ", "   "]))
