"""
La pieza nueva de esta lección: una función que se acuerda.

Corré esto:  python leccion-04/demo_closures.py
"""

from functools import partial

print("=" * 64)
print("1. UNA FUNCIÓN QUE FABRICA FUNCIONES")
print("=" * 64)


def hacer_saludador(saludo):
    def saludar(nombre):
        # `saludo` no es parámetro de `saludar` ni variable global.
        # Viene de la función de afuera, y sigue vivo cuando esta se ejecuta.
        return f"{saludo}, {nombre}!"

    return saludar  # ojo: SIN paréntesis. Devuelvo la función, no la llamo.


hola = hacer_saludador("Hola")
buenas = hacer_saludador("Buenas")

print("  hola('Ana')    ->", hola("Ana"))
print("  buenas('Luis') ->", buenas("Luis"))
print("\n  Son dos objetos distintos:", hola is not buenas)
print("  Cada uno se guardó SU saludo:")
print("    hola   capturó ->", hola.__closure__[0].cell_contents)
print("    buenas capturó ->", buenas.__closure__[0].cell_contents)
print("\n  (`__closure__` es la mochila. No la vas a usar nunca, pero acá se ve.)")

print("\n" + "=" * 64)
print("2. EL ERROR QUE TE VA A PASAR")
print("=" * 64)


def acumulador_roto():
    total = 0

    def sumar(n):
        total = total + n  # noqa: F823  ← asignar acá vuelve `total` local a `sumar`
        return total

    return sumar


try:
    acumulador_roto()(5)
except UnboundLocalError as e:
    print("  UnboundLocalError:", e)

print("""
  Leelo al revés: Python vio `total = ...` DENTRO de `sumar`, así que decidió
  que `total` es una variable local de `sumar`. Cuando llega a evaluar el lado
  derecho, esa variable local todavía no tiene valor. El `total = 0` de afuera
  quedó tapado.""")

print("=" * 64)
print("3. LA SOLUCIÓN: nonlocal")
print("=" * 64)


def hacer_acumulador():
    total = 0

    def sumar(n):
        nonlocal total  # "este nombre es de la función de afuera"
        total += n
        return total

    return sumar


acumular = hacer_acumulador()
otro = hacer_acumulador()

print("  acumular(10) ->", acumular(10))
print("  acumular(5)  ->", acumular(5))
print("  acumular(1)  ->", acumular(1))
print("\n  Y el segundo arranca de cero, no comparte nada:")
print("  otro(100)    ->", otro(100))

print("\n  Eso es estado privado sin escribir una clase.")

print("\n" + "=" * 64)
print("4. CUÁNDO **NO** HACE FALTA nonlocal")
print("=" * 64)


def hacer_registrador():
    historial = []  # una lista mutable

    def registrar(mensaje):
        # .append() NO reasigna `historial`, solo lo modifica.
        # Por eso esto anda sin nonlocal.
        historial.append(mensaje)
        return list(historial)

    return registrar


log = hacer_registrador()
print("  log('arranca') ->", log("arranca"))
print("  log('procesa') ->", log("procesa"))
print("\n  Regla: `nonlocal` es para REASIGNAR (=, +=), no para mutar.")

print("\n" + "=" * 64)
print("5. LO MISMO, PERO CON partial")
print("=" * 64)


def elevar(base, exponente):
    return base**exponente


al_cuadrado = partial(elevar, exponente=2)  # fijo el SEGUNDO, así que por nombre
dos_a_la = partial(elevar, 2)  # fijo el PRIMERO, va posicional

print("  al_cuadrado(9) ->", al_cuadrado(9))
print("  dos_a_la(10)   ->", dos_a_la(10))
print("""
  Los posicionales fijos se pegan al principio: `dos_a_la(10)` termina
  llamando a `elevar(2, 10)`. Si querés fijar uno del medio o del final,
  se fija por nombre.""")
