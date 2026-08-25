"""
Lección 01 — Solución de referencia.

LEÉ ESTO SOLO DESPUÉS de tener tus 48 tests en verde.

No es "la respuesta correcta" — tu versión también pasa los tests. Es la versión
idiomática, para que veas la diferencia entre código que funciona y código que
un pythonista escribiría. Los comentarios explican el porqué de cada elección.
"""


# ---------------------------------------------------------------------------
# 1. f-strings
# ---------------------------------------------------------------------------
def presentar(nombre: str, edad: int) -> str:
    return f"Hola, me llamo {nombre} y tengo {edad} años."


# ---------------------------------------------------------------------------
# 2. Truthiness
# ---------------------------------------------------------------------------
def describir(valor) -> str:
    # El ternario de Python se lee casi como una oración en inglés:
    #   <si es verdad> if <condición> else <si es falso>
    # Es el equivalente a `cond ? a : b` de C#, con el orden cambiado.
    return "con contenido" if valor else "vacío"


# ---------------------------------------------------------------------------
# 3. Unpacking
# ---------------------------------------------------------------------------
def intercambiar(a, b) -> tuple:
    # Los paréntesis son opcionales: lo que crea la tupla es la COMA, no ellos.
    # `return b, a` ya devuelve una tupla.
    return b, a


# ---------------------------------------------------------------------------
# 4. divmod
# ---------------------------------------------------------------------------
def segundos_a_hms(total: int) -> tuple[int, int, int]:
    # divmod(a, b) devuelve (a // b, a % b) de una sola pasada.
    # Es exactamente el par "cociente y resto" que este problema necesita dos veces.
    horas, resto = divmod(total, 3600)
    minutos, segundos = divmod(resto, 60)
    return horas, minutos, segundos


# ---------------------------------------------------------------------------
# 5. Slicing
# ---------------------------------------------------------------------------
def ultimos(items: list, n: int) -> list:
    # La trampa: items[-0:] es items[0:], o sea la lista ENTERA,
    # porque -0 == 0. Por eso el caso n == 0 necesita atenderse aparte.
    #
    # Existe una versión sin if:  return items[len(items) - n:]
    # ...pero hay que pensarla dos veces para entenderla. Esta es mejor código.
    if n == 0:
        return []
    return items[-n:]


# ---------------------------------------------------------------------------
# 6. Palíndromos
# ---------------------------------------------------------------------------
def es_palindromo(texto: str) -> bool:
    # Normalizar UNA vez y comparar. Si mañana hay que ignorar tildes o signos
    # de puntuación, se toca un solo lugar.
    limpio = texto.lower().replace(" ", "")
    return limpio == limpio[::-1]


# ---------------------------------------------------------------------------
# 7. El default mutable
# ---------------------------------------------------------------------------
def agregar_al_carrito(item: str, carrito: list[str] | None = None) -> list[str]:
    # El patrón canónico de Python. Memorizalo tal cual.
    if carrito is None:
        carrito = []
    carrito.append(item)
    return carrito


# ---------------------------------------------------------------------------
# 8. Comparaciones encadenadas
# ---------------------------------------------------------------------------
def clasificar_nota(nota: int) -> str:
    # `0 <= nota <= 10` es sintaxis válida de Python y NO existe en C#/JS.
    # Se lee igual que en matemática y evalúa `nota` una sola vez.
    if not 0 <= nota <= 10:
        return "inválida"
    # En una cadena if/elif, cada rama ya tiene descartadas todas las anteriores.
    # Por eso alcanza con el límite superior: el inferior está garantizado.
    if nota <= 3:
        return "insuficiente"
    if nota <= 6:
        return "regular"
    if nota <= 8:
        return "aprobado"
    return "excelente"


# ---------------------------------------------------------------------------
# 9. None como "no hay resultado"
# ---------------------------------------------------------------------------
def primera_palabra_larga(texto: str, minimo: int) -> str | None:
    # .split() sin argumentos parte por cualquier cantidad de espacios, tabs y
    # saltos de línea, y descarta los vacíos. .split(" ") no hace nada de eso:
    #   "hola  mundo".split(" ")  ->  ['hola', '', 'mundo']
    for palabra in texto.split():
        if len(palabra) > minimo:
            return palabra
    # Con texto vacío el for no itera y se cae acá solo: no hace falta
    # un `if not texto` al principio.
    return None


# ---------------------------------------------------------------------------
# 10. dict.get() con default
# ---------------------------------------------------------------------------
def contar_caracteres(texto: str) -> dict[str, int]:
    conteo: dict[str, int] = {}
    for letra in texto:
        if letra == " ":
            continue  # `continue` salta a la próxima vuelta del bucle
        # .get(clave, default) devuelve el default si la clave no existe,
        # en vez de lanzar KeyError. Reemplaza el if/else entero.
        conteo[letra] = conteo.get(letra, 0) + 1
    return conteo


# En la Fase 1 vas a ver que todo el ejercicio 10 es, en realidad, una línea:
#
#     from collections import Counter
#     return dict(Counter(texto.replace(" ", "")))
#
# Pero había que hacerlo a mano primero para entender qué hace Counter por dentro.
