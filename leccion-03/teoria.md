# Lección 03 — Ordenar, lambdas y `collections`

Duración: ~20 min de lectura + 40 min de ejercicios.

La 02 te cambió la forma de escribir bucles. Esta te da las herramientas que hacen que
no tengas que escribirlos casi nunca.

---

## 1. `sorted()` vs `.sort()`

```python
numeros = [3, 1, 2]

ordenados = sorted(numeros)  # devuelve una lista NUEVA; `numeros` queda igual
numeros.sort()  # ordena EN EL LUGAR; devuelve None
```

Dos errores clásicos:

```python
numeros = numeros.sort()  # ❌ numeros ahora vale None
ordenados = sorted(numeros)  # ✅
```

**Regla:** usá `sorted()` casi siempre. `.sort()` solo cuando la lista es tuya, es grande
y no te importa perder el orden original.

`sorted()` funciona sobre cualquier cosa iterable (lista, tupla, set, dict, string) y
**siempre devuelve una lista**.

---

## 2. `key=` — el corazón de esta lección

Por defecto `sorted` compara los elementos entre sí. Con `key=` le pasás una **función
que extrae el criterio** de cada elemento:

```python
palabras = ["python", "es", "genial"]

sorted(palabras)  # ['es', 'genial', 'python']   alfabético
sorted(palabras, key=len)  # ['es', 'python', 'genial']   por largo
```

Fijate que `len` va **sin paréntesis**. No estás llamando a `len`, estás pasando la
función misma para que `sorted` la llame por vos, una vez por elemento. Las funciones en
Python son valores, como en JS.

`key` no cambia lo que se devuelve, solo el criterio de comparación. La lista que sale
tiene los elementos originales.

---

## 3. `lambda` — funciones anónimas

Cuando el criterio no es una función que ya existe, la definís en el lugar:

```python
lambda p: p["edad"]
   ▲   ▲       ▲
   │   │       └── qué devuelve
   │   └── el parámetro
   └── palabra clave
```

Es el equivalente a `p => p.Edad` de C# / `p => p.edad` de JS. Una `lambda` es una función
de **una sola expresión**, sin `return` (lo devuelve implícitamente).

```python
personas = [{"nombre": "Ana", "edad": 30}, {"nombre": "Luis", "edad": 25}]

sorted(personas, key=lambda p: p["edad"])  # por edad
sorted(personas, key=lambda p: p["nombre"])  # por nombre
```

### Cuándo NO usar lambda

Una `lambda` sirve para un criterio corto que se usa una vez. Si necesitás lógica de
verdad, definí una función con nombre:

```python
# ❌ ilegible
sorted(datos, key=lambda d: (d["a"] or 0) + (d["b"] or 0) if d["tipo"] == "x" else 0)


# ✅
def puntaje(d):
    if d["tipo"] != "x":
        return 0
    return (d["a"] or 0) + (d["b"] or 0)


sorted(datos, key=puntaje)
```

Y nunca le pongas nombre a una lambda (`f = lambda x: ...`). Si necesita nombre, usá `def`.

---

## 4. `reverse=True`

```python
sorted(numeros, reverse=True)  # de mayor a menor
sorted(palabras, key=len, reverse=True)  # de más larga a más corta
```

---

## 5. Ordenar por varios criterios: la clave-tupla

Las tuplas se comparan **elemento por elemento**: primero el primero, y solo si empatan
se mira el segundo. Eso te da el orden por varios criterios gratis:

```python
sorted(productos, key=lambda p: (p["categoria"], p["precio"]))
```

Ordena por categoría; dentro de cada categoría, por precio.

### Cuando cada criterio va en dirección distinta

`reverse=True` invierte **todo**, no un criterio suelto. Para mezclar direcciones con
números, negás el que quieras al revés:

```python
# más votos primero; si empatan, alfabético ascendente
sorted(votos.items(), key=lambda item: (-item[1], item[0]))
```

`-item[1]` da vuelta el orden de ese criterio solamente. Solo sirve con números
(un string no se puede negar).

> **Dato:** el sort de Python es *estable* — los elementos que empatan conservan el orden
> que traían. Por eso otra técnica válida es ordenar dos veces, del criterio menos
> importante al más importante.

---

## 6. `min` y `max` también aceptan `key=`

```python
max(palabras, key=len)  # la palabra más larga
min(personas, key=lambda p: p["edad"])  # la persona más joven
max(
    stock.items(), key=lambda item: item[1]
)  # el par (producto, cantidad) con más stock
```

Y aceptan `default=` para no reventar con una colección vacía:

```python
max([], key=len, default=None)  # None en vez de ValueError
```

---

## 7. `Counter` — contar cosas

Acordate del ejercicio 10 de la lección 01, donde contaste caracteres a mano. Esto lo hace
por vos:

```python
from collections import Counter

Counter("casa")  # Counter({'a': 2, 'c': 1, 's': 1})
Counter(["a", "b", "a"])  # Counter({'a': 2, 'b': 1})
```

Un `Counter` **es un dict** (hereda de dict), así que todo lo que sabés de dicts funciona:
`.items()`, `.values()`, `in`, indexado. Con un extra útil:

```python
c = Counter("mississippi")
c["s"]  # 4
c["z"]  # 0   ← una clave que no existe da 0, NO revienta con KeyError
c.most_common(2)  # [('i', 4), ('s', 4)]   los N más frecuentes, ya ordenados
c.most_common()  # todos, de mayor a menor
```

Y esto resuelve en O(n) lo que en la lección 02 hiciste en O(n²) con `.count()`:

```python
{x for x, veces in Counter(items).items() if veces > 1}
```

`Counter` recorre la lista **una sola vez**. `.count()` la recorría entera por cada
elemento.

---

## 8. `defaultdict` — el dict que se autocompleta

Tu ejercicio 11 de la lección 02 usaba `setdefault`. Esto es más limpio:

```python
from collections import defaultdict

grupos = defaultdict(list)  # el argumento es la FUNCIÓN que crea el valor por defecto
for nombre in nombres:
    grupos[nombre[0].upper()].append(nombre)
```

Cuando accedés a una clave que no existe, `defaultdict` la crea llamando a la función que
le pasaste (`list` → `[]`, `int` → `0`, `set` → `set()`) en vez de lanzar `KeyError`.

```python
conteo = defaultdict(int)
for letra in texto:
    conteo[letra] += 1  # la primera vez arranca en 0, no revienta
```

⚠️ El efecto colateral: **acceder crea la clave**. Con un `defaultdict`, un simple
`grupos["Z"]` deja una lista vacía guardada bajo `"Z"`. Si eso te molesta, convertilo a
dict común antes de devolverlo: `dict(grupos)`.

---

## 9. `deque` — la cola eficiente

```python
from collections import deque

cola = deque([1, 2, 3])
cola.append(4)  # al final     O(1)
cola.appendleft(0)  # al principio O(1)
cola.pop()  # del final    O(1)
cola.popleft()  # del principio O(1)
```

¿Por qué existe? Porque en una `list`, sacar o insertar **al principio** es O(n): hay que
correr todos los demás elementos un lugar.

```python
lista.pop(0)  # O(n)  ❌ si lo hacés en un bucle, es O(n²)
deque.popleft()  # O(1)  ✅
```

Si estás implementando una cola (FIFO), usá `deque`. Para una pila (LIFO) la `list`
alcanza, porque `.append()` y `.pop()` al final ya son O(1).

---

## 10. Desempaquetado avanzado

### El `*` que junta el resto

```python
primero, *resto = [1, 2, 3, 4]  # primero=1,  resto=[2, 3, 4]
*inicio, ultimo = [1, 2, 3, 4]  # inicio=[1, 2, 3],  ultimo=4
primero, *medio, ultimo = [1, 2, 3, 4]  # medio=[2, 3]
```

`*resto` siempre recoge una **lista**, aunque a la derecha haya una tupla. Y si no queda
nada, es una lista vacía (no falla).

### Combinar dicts

```python
config_default = {"host": "localhost", "puerto": 8000}
config_usuario = {"puerto": 9000}

config_default | config_usuario  # {'host': 'localhost', 'puerto': 9000}
```

El operador `|` (Python 3.9+) devuelve un dict nuevo; **el de la derecha gana** en los
conflictos. Es la forma canónica de aplicar overrides sobre una configuración por defecto.

La forma vieja, que vas a ver en código existente, hace lo mismo:

```python
{**config_default, **config_usuario}
```

---

## Ahora sí

1. Abrí `ejercicios_03.py`
2. `pytest leccion-03 -v`
3. `ruff format leccion-03` y `ruff check leccion-03` antes de mostrármelo

Los ejercicios 8 y 9 son reescrituras de cosas que ya resolviste en las lecciones
anteriores. Compará cuánto código desaparece.
