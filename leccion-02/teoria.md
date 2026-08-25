# Lección 02 — Estructuras de datos y comprehensions

Duración: ~20 min de lectura + 40 min de ejercicios.

Esta es **la** lección donde tu código deja de parecer C# traducido. Si de todo el
roadmap solo pudieras hacer una lección, sería esta.

---

## 1. Las cuatro estructuras

| Python | Equivalente en C# | Ordenada | Mutable | Duplicados | Sintaxis |
|---|---|---|---|---|---|
| `list` | `List<T>` | Sí | Sí | Sí | `[1, 2, 3]` |
| `tuple` | `ValueTuple` / registro inmutable | Sí | **No** | Sí | `(1, 2, 3)` |
| `dict` | `Dictionary<K,V>` | Sí (por inserción) | Sí | Claves no | `{"a": 1}` |
| `set` | `HashSet<T>` | **No** | Sí | **No** | `{1, 2, 3}` |

⚠️ Cuidado con uno: `{}` **no es un set vacío**, es un dict vacío. El set vacío se
escribe `set()`. Es la única asimetría fea de la sintaxis de Python.

### Cuándo usar cada una

- **`list`** — el default. Colección ordenada que vas a recorrer o modificar.
- **`tuple`** — cuando el contenido no debe cambiar: coordenadas, un registro de la base
  de datos, el retorno múltiple de una función. Al ser inmutable, puede usarse como
  clave de un dict (una lista no puede).
- **`dict`** — cuando buscás **por identificador** en vez de por posición.
- **`set`** — cuando solo te importa la pertenencia y la unicidad. Deduplicar y preguntar
  "¿está esto acá?".

---

## 2. `in` y por qué la estructura importa (esto sí es performance real)

```python
if item in coleccion:
```

Se escribe igual para las cuatro, pero **no cuesta lo mismo**:

| Estructura | Costo de `in` | Qué hace por dentro |
|---|---|---|
| `list` | **O(n)** | Recorre elemento por elemento |
| `tuple` | **O(n)** | Idem |
| `set` | **O(1)** | Calcula el hash y va directo |
| `dict` | **O(1)** | Idem (busca en las claves) |

Con 10 elementos da igual. Con 100.000, la diferencia es de segundos a microsegundos:

```python
# ❌ si `ya_procesados` es una lista, esto es O(n²)
for item in millones_de_items:
    if item in ya_procesados:
        continue

# ✅ con un set, es O(n)
ya_procesados = set()
```

Este es el bug de performance número uno en código Python de gente que viene de otros
lenguajes. Si vas a preguntar "¿está?" muchas veces, usá un `set`.

Los sets además hacen operaciones de conjuntos:

```python
a = {1, 2, 3}
b = {3, 4, 5}

a & b    # {3}              intersección — en ambos
a | b    # {1,2,3,4,5}      unión
a - b    # {1, 2}           diferencia — en a pero no en b
a ^ b    # {1,2,4,5}        los que están en uno solo
```

---

## 3. Comprehensions — el corazón de la lección

Vos hoy escribís esto (que funciona, y así se escribe en C#):

```python
resultado = []
for n in numeros:
    resultado.append(n * 2)
```

Un pythonista escribe:

```python
resultado = [n * 2 for n in numeros]
```

### Anatomía

```
[  n * 2   for n in numeros  ]
   ▲             ▲
   │             └── de dónde saco cada elemento
   └── qué hago con cada uno
```

Se lee de **derecha a izquierda**: "para cada n en números, dame n por 2".

Es lo mismo que `numeros.Select(n => n * 2).ToList()` de LINQ, pero es sintaxis del
lenguaje, no una librería.

### Con filtro

```python
[n for n in numeros if n % 2 == 0]        # solo los pares
[n * 2 for n in numeros if n > 0]         # filtra y transforma
```

El `if` al final **filtra**: los que no cumplen no entran. Equivale a
`.Where(...).Select(...)` de LINQ.

⚠️ Ojo con la posición del `if`. Al final = filtro. En el medio = ternario:

```python
[n for n in nums if n > 0]              # filtra: descarta los negativos
[n if n > 0 else 0 for n in nums]       # transforma: convierte negativos en 0
```

La primera puede devolver menos elementos. La segunda siempre devuelve la misma cantidad.

### También hay de dict y de set

```python
{palabra: len(palabra) for palabra in palabras}   # dict comprehension
{palabra.lower() for palabra in palabras}         # set comprehension (deduplica)
```

Cambiás los corchetes por llaves. Si hay `clave: valor`, es un dict; si no, un set.

### Anidadas (usar con moderación)

```python
matriz = [[1, 2], [3, 4], [5, 6]]
[n for fila in matriz for n in fila]      # [1, 2, 3, 4, 5, 6]
```

Los `for` van en el **mismo orden** que si los escribieras anidados:

```python
for fila in matriz:        # primer for
    for n in fila:         # segundo for
        ...
```

Se lee de izquierda a derecha en los `for`. Es la parte menos intuitiva de la sintaxis.

### Cuándo NO usar una comprehension

Una comprehension sirve para **construir una colección**. Si tenés tres niveles de
anidamiento, condiciones complicadas o necesitás un `try/except`, escribí el `for` de
toda la vida. Un bucle claro le gana a una comprehension ilegible.

Y nunca uses una comprehension solo por su efecto colateral:

```python
[print(x) for x in items]     # ❌ construye una lista de None al pedo
for x in items: print(x)      # ✅
```

---

## 4. `enumerate` — índice y valor a la vez

```python
# ❌ lo que hace todo el mundo al llegar de C#
for i in range(len(items)):
    print(i, items[i])

# ✅ pythónico
for i, item in enumerate(items):
    print(i, item)

# arrancando en 1
for i, item in enumerate(items, start=1):
    print(i, item)
```

`enumerate` devuelve tuplas `(índice, elemento)` y el `for` las desempaqueta sola.

**Regla:** si escribís `range(len(algo))`, casi seguro querías `enumerate`.

---

## 5. `zip` — recorrer dos colecciones en paralelo

```python
nombres = ["Ana", "Luis", "Sofi"]
edades = [30, 25, 41]

for nombre, edad in zip(nombres, edades):
    print(f"{nombre} tiene {edad}")
```

`zip` corta con la **más corta**: si una lista tiene 3 elementos y la otra 5, obtenés 3.

Y combinado con `dict()` es la forma canónica de armar un diccionario desde dos listas:

```python
dict(zip(nombres, edades))     # {'Ana': 30, 'Luis': 25, 'Sofi': 41}
```

---

## 6. Recorrer un dict

```python
stock = {"pan": 3, "leche": 0, "queso": 7}

for clave in stock:                       # por defecto recorre las CLAVES
    ...
for clave in stock.keys():                # explícito, lo mismo
    ...
for valor in stock.values():              # solo los valores
    ...
for clave, valor in stock.items():        # ambos ← el que más vas a usar
    ...
```

`.items()` te da tuplas `(clave, valor)`. Es el equivalente a recorrer un
`Dictionary<K,V>` con `KeyValuePair`, pero desempaquetado directo.

Combinado con dict comprehension:

```python
{k: v for k, v in stock.items() if v > 0}    # solo los que tienen stock
```

---

## 7. Funciones que operan sobre colecciones

```python
sum([1, 2, 3])            # 6
min([3, 1, 2])            # 1
max([3, 1, 2])            # 3
len(coleccion)            # cantidad
sorted([3, 1, 2])         # [1, 2, 3]  ← devuelve una lista NUEVA
any([False, True])        # True   ¿alguno es verdadero?
all([True, True])         # True   ¿todos son verdaderos?
```

`any` y `all` combinados con comprehensions son muy expresivos:

```python
if any(p["precio"] > 1000 for p in productos):     # ¿hay algún producto caro?
if all(n > 0 for n in numeros):                    # ¿son todos positivos?
```

(Sin corchetes adentro se llama *generator expression* — no construye la lista entera
en memoria y corta apenas sabe la respuesta. Lo vemos en la Fase 5.)

---

## Ahora sí

1. Abrí `ejercicios.py`
2. **Regla de esta lección: no uses `.append()` en un bucle.** Si te encontrás haciendo
   `lista = []` seguido de un `for` con `.append()`, pará y convertilo en comprehension.
   (Hay **una sola** excepción justificada, el ejercicio 11, y ahí te aviso.)
3. `pytest leccion-02 -v`
4. `ruff format leccion-02` antes de mostrármelo
