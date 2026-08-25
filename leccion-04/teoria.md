# Lección 04 — Funciones flexibles, funciones como valores, closures

Duración: ~20 min de lectura + 40 min de ejercicios.

Arranca la **Fase 2**. Hasta acá las funciones fueron cajas que recibían datos y
devolvían datos. En esta fase las funciones pasan a ser **datos ellas mismas**: se
guardan en variables, se pasan como argumento, se devuelven, se envuelven.

Esta lección te da las tres piezas. La 05 las usa para construir decoradores.

---

## 1. Los parámetros de Python, en orden

En C# resolvés "esta función acepta varias formas de llamarse" con **sobrecarga**: tres
métodos con el mismo nombre y distinta firma. En Python no existe la sobrecarga. Una
función, una firma — pero la firma es mucho más expresiva.

```python
def conectar(host, puerto=5432, *, timeout=30): ...
```

- `host` → **posicional obligatorio**
- `puerto=5432` → tiene default, se puede omitir
- `timeout=30` → está después del `*`, así que es **keyword-only**: `conectar("db", timeout=5)`
  funciona, `conectar("db", 5432, 5)` es `TypeError`

Y al llamar, cualquier parámetro se puede pasar por nombre:

```python
conectar("db")
conectar("db", 6000)
conectar(host="db", puerto=6000)
conectar(puerto=6000, host="db")  # el orden no importa si van todos por nombre
```

> Recordatorio de la lección 01: el default se evalúa **una sola vez**, al definir la
> función. Por eso `def f(items=[])` es una bomba. Ya lo sabés — solo no te olvides
> cuando escribas los ejercicios.

---

## 2. `*args` — "y todos los posicionales que vengan"

```python
def sumar(*numeros):
    return sum(numeros)


sumar(1, 2)  # 3
sumar(1, 2, 3, 4)  # 10
sumar()  # 0
```

Adentro de la función, `numeros` es una **tupla**. Siempre. Aunque le pases un solo
argumento, aunque no le pases ninguno (ahí es `()`).

El nombre `args` es pura convención; lo que hace el trabajo es el `*`. `*numeros` se lee
mejor y es igual de válido.

⚠️ Que sea una tupla significa que es **inmutable**: no podés hacer `numeros.append(...)`.
Si necesitás modificarla, convertila: `list(numeros)`.

---

## 3. `**kwargs` — "y todos los nombrados que vengan"

```python
def describir(**atributos):
    return atributos


describir(color="rojo", peso=3)  # {'color': 'rojo', 'peso': 3}
describir()  # {}
```

`atributos` es un **dict** común: claves los nombres, valores los valores. Las claves son
siempre strings.

---

## 4. La firma completa

El orden es fijo y no se negocia:

```python
def f(posicional, con_default=1, *args, keyword_only, otro_kw=2, **kwargs): ...
```

En la práctica casi nunca los vas a usar todos juntos. Lo que sí vas a ver mucho:

```python
def envoltorio(*args, **kwargs):
    return func(*args, **kwargs)
```

Esa firma significa **"acepto lo que sea"**. Es la firma de todo envoltorio genérico, y
es exactamente la que vas a usar en la lección 05.

### El `*` solo, sin nombre

```python
def crear_usuario(nombre, *, admin=False): ...
```

El `*` pelado marca "de acá en adelante, todo va por nombre". Se usa para que nadie
escriba `crear_usuario("ana", True)` — un booleano suelto en una llamada no dice nada.
`crear_usuario("ana", admin=True)` se lee solo.

---

## 5. El mismo `*`, del otro lado: desempaquetar al llamar

Esto es la otra mitad, y es la que más se olvida. En la **definición**, `*` recoge. En la
**llamada**, `*` reparte:

```python
def punto(x, y, z):
    return f"({x}, {y}, {z})"


coords = [1, 2, 3]

punto(coords)  # ❌ TypeError: falta y, falta z (le pasaste UNA lista)
punto(*coords)  # ✅ "(1, 2, 3)"  — equivale a punto(1, 2, 3)
```

Y con dicts, `**`:

```python
config = {"x": 1, "y": 2, "z": 3}
punto(**config)  # ✅ equivale a punto(x=1, y=2, z=3)
```

Las claves del dict tienen que coincidir con los nombres de los parámetros. Si sobra una
clave, es `TypeError`.

**El truco mental:** un `*` en una llamada convierte una colección en argumentos sueltos.
Un `*` en una definición convierte argumentos sueltos en una colección. Es la misma
operación en las dos direcciones.

---

## 6. Las funciones son objetos

Esto ya lo viste en JS, pero en Python se usa más y llega más lejos.

```python
def saludar(nombre):
    return f"Hola, {nombre}"


f = saludar  # sin paréntesis: NO la llamo, la guardo
f("Ana")  # 'Hola, Ana'
```

`saludar` es un objeto como cualquier otro. Va en listas, en dicts, se pasa como
argumento, se devuelve. Ya lo usaste sin pensarlo: `sorted(palabras, key=len)`.

Como es un objeto, tiene atributos:

```python
saludar.__name__  # 'saludar'   ← el nombre con el que se definió
saludar.__doc__  # su docstring
```

Y le podés **colgar atributos propios**, igual que a cualquier objeto:

```python
saludar.veces_usada = 0
saludar.veces_usada += 1
```

Parece un truco raro. Es la forma estándar de que un envoltorio exponga un dato hacia
afuera, y la vas a usar en el ejercicio 10.

### El dispatch table: el reemplazo del `switch`

Python no tiene `switch`. La cadena de `if/elif` funciona, pero cuando lo único que
cambia es *qué función se llama*, hay algo mejor:

```python
# ❌ el reflejo de C#
def formatear(tipo, valor):
    if tipo == "mayus":
        return valor.upper()
    elif tipo == "minus":
        return valor.lower()
    elif tipo == "titulo":
        return valor.title()
    return valor


# ✅ un dict de funciones
FORMATOS = {"mayus": str.upper, "minus": str.lower, "titulo": str.title}


def formatear(tipo, valor):
    accion = FORMATOS.get(tipo)
    if accion is None:
        return valor
    return accion(valor)
```

Agregar un formato nuevo es agregar una línea al dict, no tocar la función. Y fijate en
`FORMATOS.get(tipo)` con `is None`: acá `None` es centinela, no truthiness.

> `str.upper`, sin paréntesis y sin instancia, es la función "método de string" suelta.
> `str.upper("hola")` es lo mismo que `"hola".upper()`.

---

## 7. Closures — funciones que fabrican funciones

Una función definida adentro de otra **se acuerda** de las variables de la de afuera,
incluso después de que la de afuera terminó. Eso es un closure.

```python
def hacer_saludador(saludo):
    def saludar(nombre):
        return f"{saludo}, {nombre}!"

    return saludar  # devuelvo la función, NO la llamo


hola = hacer_saludador("Hola")
buenas = hacer_saludador("Buenas")

hola("Ana")  # 'Hola, Ana!'
buenas("Luis")  # 'Buenas, Luis!'
```

`hacer_saludador` ya terminó de ejecutarse, pero `saludo` sigue vivo adentro de `saludar`.
Cada llamada a `hacer_saludador` crea un `saludo` **independiente**: `hola` y `buenas` no
comparten nada.

Viniendo de C#: es lo mismo que capturar una variable en una lambda. La diferencia es
cuánto se usa. En Python un closure es la forma normal de **configurar** una función: en
vez de pasarle el mismo parámetro veinte veces, fabricás una versión que ya lo tiene
adentro.

### `nonlocal` — cuando el closure necesita *cambiar* lo que capturó

Leer la variable de afuera sale gratis. Asignarla, no:

```python
def hacer_acumulador():
    total = 0

    def sumar(n):
        total = total + n  # ❌ UnboundLocalError
        return total

    return sumar
```

Falla porque **asignarle a un nombre lo vuelve local a esa función**. Al ver `total = ...`
adentro de `sumar`, Python decide que `total` es una variable local de `sumar` — y del
lado derecho todavía no tiene valor.

`nonlocal` deshace eso: "este nombre no es mío, es de la función de afuera".

```python
def hacer_acumulador():
    total = 0

    def sumar(n):
        nonlocal total
        total += n
        return total

    return sumar


acumular = hacer_acumulador()
acumular(10)  # 10
acumular(5)  # 15
acumular(1)  # 16
```

Ahí tenés estado privado sin escribir una clase. Es el equivalente a un campo privado con
un método público, en cinco líneas.

> No confundas `nonlocal` con `global`. `nonlocal` sube **un nivel de función**. `global`
> va directo al módulo. `global` casi siempre es un error de diseño.

⚠️ `nonlocal` hace falta solo para **reasignar** (`=`, `+=`). Si lo capturado es una lista
y hacés `items.append(x)`, no estás reasignando nada: eso anda sin `nonlocal`.

Corré `python leccion-04/demo_closures.py` antes de los ejercicios. Se ve mejor que leerlo.

---

## 8. `functools.partial` — congelar argumentos

Cuando el closure que querés escribir es solo "esta función, pero con un argumento ya
puesto", hay un atajo:

```python
from functools import partial

potencia_de_2 = partial(pow, 2)  # pow(2, n): 2 elevado a n
potencia_de_2(10)  # 1024

redondear_centavos = partial(round, ndigits=2)
redondear_centavos(3.14159)  # 3.14
```

`partial(func, *fijos, **fijos_por_nombre)` devuelve una función nueva que, al llamarse,
llama a `func` con los argumentos fijos **más** los que le pases en el momento.

Los posicionales fijos se pegan **al principio**. Por eso, cuando lo que querés fijar no
es el primer parámetro, se fija por nombre (`ndigits=2`).

### `partial` o closure, ¿cuál?

- Si la función que querés especializar **ya existe** → `partial`. Una línea.
- Si necesitás lógica propia, o estado que cambia → closure con `def`.

---

## 9. Type hints para funciones

Cuando un parámetro es una función, el tipo es `Callable`:

```python
from collections.abc import Callable


def aplicar(func: Callable[[int], str], n: int) -> str:
    return func(n)
```

`Callable[[int], str]` se lee "función que toma un int y devuelve un str". La lista de
adentro son los parámetros.

Si no te importa la firma, `Callable` solo alcanza. En estos ejercicios usamos la forma
suelta: ahora lo importante es el mecanismo, no el tipado fino (eso es la Fase 6).

---

## Ahora sí

1. `python leccion-04/demo_closures.py` — 2 minutos, aclara la sección 7
2. Abrí `ejercicios_04.py`
3. `pytest leccion-04 -v`
4. `ruff format leccion-04` y `ruff check leccion-04` antes de mostrármelo

El ejercicio 12 es una reescritura: dos funciones de la lección 03 se convierten en una
sola. El 10 es el puente a los decoradores — cuando lo termines, ya vas a haber escrito
uno sin saberlo.
