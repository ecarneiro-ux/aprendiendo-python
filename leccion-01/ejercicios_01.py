"""
Lección 01 — Ejercicios.

Completá cada función reemplazando el `...` por tu código.
Corré los tests con:  pytest leccion-01 -v

No borres las firmas ni los type hints.
"""


# ---------------------------------------------------------------------------
# 1. Calentamiento — f-strings
# ---------------------------------------------------------------------------
def presentar(nombre: str, edad: int) -> str:
    """Devuelve exactamente: 'Hola, me llamo Ana y tengo 30 años.'

    >>> presentar("Ana", 30)
    'Hola, me llamo Ana y tengo 30 años.'
    """
    return f"Hola, me llamo {nombre} y tengo {edad} años."


# ---------------------------------------------------------------------------
# 2. Truthiness — nada de len() > 0
# ---------------------------------------------------------------------------
def describir(valor) -> str:
    """Devuelve 'vacío' si el valor es falsy, 'con contenido' si es truthy.

    Usá la truthiness directamente. Si escribís `len(valor) > 0` va a fallar
    con los enteros y con None.
    """
    if valor:
        return "con contenido"
    else:
        return "vacío"


# ---------------------------------------------------------------------------
# 3. Unpacking
# ---------------------------------------------------------------------------
def intercambiar(a, b) -> tuple:
    """Devuelve una tupla con los dos valores en orden inverso.

    Hacelo en UNA línea, sin variable temporal.

    >>> intercambiar(1, 2)
    (2, 1)
    """
    return (b, a)


# ---------------------------------------------------------------------------
# 4. División entera y módulo — devolver varios valores
# ---------------------------------------------------------------------------
def segundos_a_hms(total: int) -> tuple[int, int, int]:
    """Convierte segundos a (horas, minutos, segundos).

    >>> segundos_a_hms(3725)
    (1, 2, 5)
    """
    horas = total // 3600
    resto_segundos = total % 3600
    minutos = resto_segundos // 60
    segundos = resto_segundos % 60

    return (horas, minutos, segundos)


# ---------------------------------------------------------------------------
# 5. Slicing
# ---------------------------------------------------------------------------
def ultimos(items: list, n: int) -> list:
    """Devuelve los últimos n elementos de la lista.

    Si n es mayor que el largo de la lista, devolvé la lista entera.
    Si n es 0, devolvé una lista vacía.
    Resolvelo con slicing, sin bucles ni ifs.

    >>> ultimos([1, 2, 3, 4, 5], 2)
    [4, 5]
    """
    if n == 0:
        return []
    else:
        return items[-n:]


# ---------------------------------------------------------------------------
# 6. Slicing — palíndromos
# ---------------------------------------------------------------------------
def es_palindromo(texto: str) -> bool:
    """True si el texto se lee igual al derecho y al revés.

    Ignorá mayúsculas/minúsculas y los espacios.

    >>> es_palindromo("Anita lava la tina")
    True
    """
    return texto.lower().replace(" ", "") == texto[::-1].lower().replace(" ", "")


# ---------------------------------------------------------------------------
# 7. LA TRAMPA — argumento por defecto mutable
# ---------------------------------------------------------------------------
def agregar_al_carrito(item: str, carrito: list[str] | None = None) -> list[str]:
    """Agrega el item al carrito y lo devuelve.

    Si no se pasa carrito, se crea uno nuevo VACÍO en cada llamada.
    (Releé la sección 5 de la teoría si dudás.)

    >>> agregar_al_carrito("pan")
    ['pan']
    >>> agregar_al_carrito("leche")
    ['leche']
    """
    if carrito is None:
        carrito = []
    carrito.append(item)
    return carrito


# ---------------------------------------------------------------------------
# 8. Ternario pythónico + if/elif
# ---------------------------------------------------------------------------
def clasificar_nota(nota: int) -> str:
    """Clasifica una nota de 0 a 10.

    - 9 o 10  -> 'excelente'
    - 7 u 8   -> 'aprobado'
    - 4 a 6   -> 'regular'
    - 0 a 3   -> 'insuficiente'
    - fuera del rango 0-10 -> 'inválida'
    """
    if nota < 0 or nota > 10:
        return "inválida"
    elif nota <= 3:
        return "insuficiente"
    elif nota <= 6:
        return "regular"
    elif nota >= 7 and nota <= 8:
        return "aprobado"
    else:
        return "excelente"


# ---------------------------------------------------------------------------
# 9. Devolver None explícitamente
# ---------------------------------------------------------------------------
def primera_palabra_larga(texto: str, minimo: int) -> str | None:
    """Devuelve la primera palabra con MÁS de `minimo` caracteres.

    Si no hay ninguna, devolvé None.

    >>> primera_palabra_larga("el gato negro duerme", 4)
    'negro'
    """

    palabras = texto.split(" ")
    for palabra in palabras:
        if len(palabra) > minimo:
            return palabra
    return None


# ---------------------------------------------------------------------------
# 10. Construir un dict (anticipo de la Fase 1)
# ---------------------------------------------------------------------------
def contar_caracteres(texto: str) -> dict[str, int]:
    """Cuenta cuántas veces aparece cada carácter.

    Ignorá los espacios. No uses `collections.Counter` todavía —
    hacelo a mano para entender el mecanismo.

    >>> contar_caracteres("casa")
    {'c': 1, 'a': 2, 's': 1}
    """
    conteo = {}
    for letra in texto:
        if letra != " ":
            if letra in conteo:
                conteo[letra] += 1
            else:
                conteo[letra] = 1
    return conteo
