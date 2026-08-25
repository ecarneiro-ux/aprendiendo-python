"""
Rampa de arranque para el ejercicio 1.

El ejercicio pide tres cosas a la vez. Acá van de a una.
Completá un paso, corré el archivo, y te dice si vas bien:

    python leccion-05/arranque_ej1.py

Cuando los tres estén en verde, el ejercicio 1 es el PASO 3 copiado tal cual.
Este archivo no lo mira nadie: es tuyo para romperlo.
"""

from functools import wraps  # noqa: F401  (lo vas a necesitar en el PASO 3)

# ===========================================================================
# PASO 1 — Un envoltorio para funciones SIN argumentos
# ===========================================================================
# Olvidate de *args, de **kwargs y del @. Solo esto:
#
#   sin_espacios_v1 recibe una función que no toma argumentos y devuelve un
#   string. Tenés que devolver OTRA función que, cuando la llamen, llame a la
#   original y le saque los espacios de los bordes.
#
# Adentro de `envoltorio` necesitás dos cosas:
#   1. llamar a func  (ojo: `func` es la función, `func()` es el resultado)
#   2. devolver ese resultado con .strip() aplicado
#
# Ya está escrito el `return envoltorio` de abajo. Ese está bien: devolvés la
# función SIN llamarla, igual que en `hacer_multiplicador` de la lección 04.


def sin_espacios_v1(func):
    def envoltorio():
        return func().strip()  # ← escribí acá

    return envoltorio


# ===========================================================================
# PASO 2 — Que sirva para CUALQUIER función, tome los argumentos que tome
# ===========================================================================
# El paso 1 solo anda con funciones sin argumentos. Si la decorada fuera
#   def unir(a, b, separador=" ")
# tu envoltorio no tiene por dónde recibir esos argumentos ni cómo pasárselos.
#
# La firma ya está puesta: `*args, **kwargs` significa "acepto lo que sea".
# Lo que falta es reenviárselos a func al llamarla (el * y el ** del lado de
# la LLAMADA, sección 5 de la lección 04).
#
# Copiá lo del paso 1 y agregale eso.


def sin_espacios_v2(func):
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs).strip()  # ← escribí acá

    return envoltorio


# ===========================================================================
# PASO 3 — Que no le pise la identidad a la función decorada
# ===========================================================================
# Copiá el paso 2 y agregale UNA línea: `@wraps(func)` justo arriba del
# `def envoltorio`. Nada más.
#
# (Sí: le estás poniendo un decorador a tu decorador. Es raro la primera vez.)


def sin_espacios_v3(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs).strip()  # ← escribí acá

    return envoltorio


# ===========================================================================
# De acá para abajo no toques nada: es el que te corrige.
# ===========================================================================
def diagnosticar(obtenido, esperado):
    if obtenido == esperado:
        return True, "funciona"
    if callable(obtenido):
        return False, (
            "devolviste una FUNCIÓN, no un resultado.\n"
            "        Te faltan los paréntesis: `func` es la función, `func()` la llama."
        )
    if obtenido is None:
        return False, (
            "devolviste None.\n        ¿Le pusiste `return` adentro de `envoltorio`?"
        )
    if isinstance(obtenido, str) and obtenido.strip() == esperado:
        return False, (
            f"devolviste {obtenido!r}.\n"
            "        Llamaste bien a func, pero no le sacaste los espacios: falta .strip()"
        )
    return False, f"devolviste {obtenido!r} y se esperaba {esperado!r}."


def leer_nombre():
    return "  Ana  "


def unir(a, b, separador=" "):
    return f"  {a}{separador}{b}  "


if __name__ == "__main__":
    print("=" * 64)

    # --- PASO 1 -----------------------------------------------------------
    try:
        v1 = sin_espacios_v1(leer_nombre)
        ok, detalle = diagnosticar(v1(), "Ana")
    except Exception as e:  # noqa: BLE001  (es el corrector: acá quiero atrapar todo)
        ok, detalle = False, f"reventó con {type(e).__name__}: {e}"
    print(f"PASO 1  {'OK   ' if ok else 'FALLA'}  {detalle}")

    # --- PASO 2 -----------------------------------------------------------
    try:
        v2 = sin_espacios_v2(unir)
        ok, detalle = diagnosticar(v2("Ana", "Perez", separador="-"), "Ana-Perez")
        pistas_propias = ("paréntesis", "None", "strip()")
        if not ok and not any(p in detalle for p in pistas_propias):
            detalle += "\n        (¿le pasaste *args y **kwargs a func al llamarla?)"
    except TypeError as e:
        ok, detalle = (
            False,
            (
                f"reventó con TypeError: {e}\n"
                "        Traducción: llamaste a func() sin pasarle los argumentos que recibiste."
            ),
        )
    except Exception as e:  # noqa: BLE001  (es el corrector: acá quiero atrapar todo)
        ok, detalle = False, f"reventó con {type(e).__name__}: {e}"
    print(f"PASO 2  {'OK   ' if ok else 'FALLA'}  {detalle}")

    # --- PASO 3 -----------------------------------------------------------
    try:
        v3 = sin_espacios_v3(leer_nombre)
        ok_valor, detalle = diagnosticar(v3(), "Ana")
        if ok_valor:
            nombre = v3.__name__
            ok = nombre == "leer_nombre"
            detalle = (
                "funciona y conserva el nombre"
                if ok
                else f"anda, pero __name__ vale {nombre!r} en vez de 'leer_nombre'.\n"
                "        Falta @wraps(func) arriba del def envoltorio."
            )
        else:
            ok = False
    except Exception as e:  # noqa: BLE001  (es el corrector: acá quiero atrapar todo)
        ok, detalle = False, f"reventó con {type(e).__name__}: {e}"
    print(f"PASO 3  {'OK   ' if ok else 'FALLA'}  {detalle}")

    print("=" * 64)
    print("Con los tres en verde, el ejercicio 1 ES el paso 3.")
    print("Y los ejercicios 2, 9 y 10 usan exactamente el mismo molde.")
