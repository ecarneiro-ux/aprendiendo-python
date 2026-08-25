"""
Demo: la trampa del argumento por defecto mutable.

Corré esto:  python leccion-01/demo_mutable_default.py

No hace falta que entiendas el código de la demo, solo mirá la salida.
"""

print("=" * 70)
print("PARTE 1 — ¿Cuándo se evalúa el valor por defecto?")
print("=" * 70)


def crear_lista_vacia():
    print("   >>> se está EVALUANDO el valor por defecto <<<")
    return []


print("\nAhora Python va a leer la línea 'def acumular(...)':")


def acumular(item, bolsa=crear_lista_vacia()):  # noqa: B008  el bug es a propósito
    bolsa.append(item)
    return bolsa


print("...y ya está. Fijate que el mensaje salió UNA sola vez, ANTES")
print("de que llamemos a la función ni una sola vez.\n")

print("Ahora la llamo 3 veces:")
print("  llamada 1 ->", acumular("a"))
print("  llamada 2 ->", acumular("b"))
print("  llamada 3 ->", acumular("c"))
print("\nEl mensaje NO volvió a salir. El [] se creó una vez y nunca más.")


print("\n" + "=" * 70)
print("PARTE 2 — El default vive PEGADO a la función")
print("=" * 70)


def agregar_roto(item, carrito=[]):  # noqa: B006  el bug es a propósito
    carrito.append(item)
    return carrito


print("\nAntes de llamarla, espiamos la función por dentro:")
print("  agregar_roto.__defaults__ =", agregar_roto.__defaults__)
print("  id de esa lista:", id(agregar_roto.__defaults__[0]))

print("\nLlamada 1:", agregar_roto("pan"))
print("  agregar_roto.__defaults__ =", agregar_roto.__defaults__, " <-- ¡CAMBIÓ!")

print("\nLlamada 2:", agregar_roto("leche"))
print("  agregar_roto.__defaults__ =", agregar_roto.__defaults__)

print("\nLlamada 3:", agregar_roto("queso"))
print("  agregar_roto.__defaults__ =", agregar_roto.__defaults__)
print("  id de esa lista:", id(agregar_roto.__defaults__[0]), " <-- el MISMO id")

print("\nEl 'carrito nuevo' de cada llamada es siempre el mismo objeto.")
print("No hay tres carritos. Hay UNO solo que crece para siempre.")


print("\n" + "=" * 70)
print("PARTE 3 — La versión correcta, con la misma prueba")
print("=" * 70)


def agregar_ok(item, carrito=None):
    if carrito is None:
        carrito = []          # <-- ESTA línea sí corre en CADA llamada
    carrito.append(item)
    return carrito


print("\n  agregar_ok.__defaults__ =", agregar_ok.__defaults__)

# OJO: guardamos cada resultado en una variable. Si hiciéramos
# id(agregar_ok("pan")) suelto, la lista se destruiría al instante y Python
# reutilizaría la misma dirección de memoria para la siguiente, dando ids
# iguales por casualidad. Hay que mantenerlas vivas para compararlas.
r1 = agregar_ok("pan")
r2 = agregar_ok("leche")
r3 = agregar_ok("queso")

print("\nLlamada 1:", r1, "  id:", id(r1))
print("Llamada 2:", r2, "  id:", id(r2))
print("Llamada 3:", r3, "  id:", id(r3))
print("\n  agregar_ok.__defaults__ =", agregar_ok.__defaults__, " <-- nunca cambia")
print("\n  ¿r1 y r2 son el MISMO objeto?", r1 is r2)
print("\nCada llamada devolvió una lista distinta. Correcto.")


print("\n" + "=" * 70)
print("PARTE 4 — ¿Por qué con un int NO pasa?")
print("=" * 70)


def sumar(n, total=0):
    total += n        # esto NO muta el 0: crea un int nuevo y reapunta 'total'
    return total


print("\n  sumar(5) ->", sumar(5))
print("  sumar(5) ->", sumar(5))
print("  sumar(5) ->", sumar(5))
print("  sumar.__defaults__ =", sumar.__defaults__, " <-- sigue siendo 0")
print("\nEl 0 también se crea una sola vez... pero los int son INMUTABLES.")
print("'total += n' no modifica el 0, crea un número nuevo.")
print("La lista, en cambio, se puede modificar en el lugar con .append().")
print("\nESE es el punto: el problema no es 'el default se crea una vez'.")
print("El problema es 'se crea una vez' + 'se puede modificar en el lugar'.")
