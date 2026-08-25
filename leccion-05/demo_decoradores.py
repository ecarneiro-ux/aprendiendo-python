"""
Decoradores, vistos por dentro.

Corré esto:  python leccion-05/demo_decoradores.py
"""

from functools import cache, wraps

print("=" * 64)
print("1. EL @ ES AZÚCAR: LAS DOS FORMAS SON LA MISMA")
print("=" * 64)


def anunciar(func):
    def envoltorio(*args, **kwargs):
        print(f"      -> entrando a {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"      <- saliendo de {func.__name__}")
        return resultado

    return envoltorio


def saludar_largo(nombre):
    return f"Hola, {nombre}"


saludar_largo = anunciar(saludar_largo)  # la forma larga, a mano


@anunciar  # la forma corta: hace exactamente lo de arriba
def saludar_corto(nombre):
    return f"Hola, {nombre}"


print("  forma larga:")
print("     ", saludar_largo("Ana"))
print("  forma corta (@):")
print("     ", saludar_corto("Ana"))

print("\n" + "=" * 64)
print("2. EL DECORADOR CORRE AL DEFINIR, NO AL LLAMAR")
print("=" * 64)


def ruidoso(func):
    print(f"      [decorando {func.__name__} — esto pasa AHORA, al leer el def]")
    return func


@ruidoso
def tarea():
    return "hecho"


print("  ...y recién acá la llamo:", tarea())
print("  Fijate que el mensaje de arriba salió antes. Se aplicó una sola vez.")

print("\n" + "=" * 64)
print("3. EL DECORADOR PISA LA IDENTIDAD DE LA FUNCIÓN")
print("=" * 64)


def sin_wraps(func):
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs)

    return envoltorio


def con_wraps(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs)

    return envoltorio


@sin_wraps
def pesar(kilos):
    """Devuelve los kilos."""
    return kilos


@con_wraps
def medir(metros):
    """Devuelve los metros."""
    return metros


print("  SIN wraps:")
print("    __name__ ->", pesar.__name__)
print("    __doc__  ->", pesar.__doc__)
print("  CON wraps:")
print("    __name__ ->", medir.__name__)
print("    __doc__  ->", medir.__doc__)
print("""
  El de arriba se llama 'envoltorio' porque, después del @, el nombre `pesar`
  APUNTA al envoltorio. pytest, FastAPI y los tracebacks leen __name__.
  Por eso: todo decorador que envuelve lleva @wraps(func).""")

print("=" * 64)
print("4. DECORADOR CON PARÁMETROS: LOS TRES NIVELES")
print("=" * 64)


def prefijo(texto):  # 1) los PARÁMETROS del decorador
    print(f"      [nivel 1: me llamaron con texto={texto!r}]")

    def decorador(func):  # 2) la FUNCIÓN decorada
        print(f"      [nivel 2: me toca decorar {func.__name__}]")

        @wraps(func)
        def envoltorio(*args, **kwargs):  # 3) los ARGUMENTOS de cada llamada
            return texto + func(*args, **kwargs)

        return envoltorio

    return decorador


@prefijo("LOG: ")
def mensaje(texto):
    return texto


print("  mensaje('arrancó') ->", mensaje("arrancó"))
print("""
  Los niveles 1 y 2 corrieron una sola vez, al definir. El 3 corre en cada
  llamada. Desazucarado:  mensaje = prefijo("LOG: ")(mensaje)""")

print("=" * 64)
print("5. APILADOS: SE APLICAN DE ABAJO HACIA ARRIBA")
print("=" * 64)


def negrita(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        return "**" + func(*args, **kwargs) + "**"

    return envoltorio


def cursiva(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        return "_" + func(*args, **kwargs) + "_"

    return envoltorio


@negrita
@cursiva
def texto_a():
    return "hola"


@cursiva
@negrita
def texto_b():
    return "hola"


print("  @negrita sobre @cursiva ->", texto_a())
print("  @cursiva sobre @negrita ->", texto_b())
print("""
  Se apilan como paréntesis: el de ABAJO queda ADENTRO.
    texto_a = negrita(cursiva(texto_a))
    texto_b = cursiva(negrita(texto_b))""")

print("=" * 64)
print("6. @cache: LA MEMOIZACIÓN QUE NO TENÉS QUE ESCRIBIR")
print("=" * 64)


@cache
def consultar_precio(producto):
    print(f"      [consultando {producto} en el sistema lento...]")
    return len(producto) * 100


print("  primera vez  ->", consultar_precio("teclado"))
print("  segunda vez  ->", consultar_precio("teclado"))
print("  otro producto->", consultar_precio("mouse"))
print("\n ", consultar_precio.cache_info())
print("""
  El cuerpo se ejecutó 2 veces para 3 llamadas. La clave del caché son los
  argumentos, así que TIENEN que ser hashables: una lista revienta.""")

try:
    consultar_precio(["teclado"])
except TypeError as e:
    print("  consultar_precio(['teclado']) -> TypeError:", e)
