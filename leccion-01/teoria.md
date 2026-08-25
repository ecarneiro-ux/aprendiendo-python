# Lección 01 — Python para alguien que ya programa

Duración: ~15 min de lectura + 30 min de ejercicios.

No te voy a explicar qué es una variable. Te voy a explicar **en qué Python te va a traicionar**
si asumís que funciona como C# o TypeScript.

---

## 1. Los tipos existen, pero no se declaran (y aun así los vas a escribir)

```python
nombre = "Emiliano"        # Python infiere str
edad = 34                  # int
```

Pero Python tiene *type hints* opcionales, y en código profesional se usan siempre:

```python
def saludar(nombre: str, edad: int) -> str:
    return f"Hola {nombre}, tenés {edad}"
```

**Importante:** los type hints **no se validan en runtime**. Nada te impide llamar
`saludar(123, "hola")` y Python lo ejecuta feliz. Son para vos, para tu editor y para
herramientas como `mypy`. Es lo contrario a C#, donde el compilador te frena.

Los usamos igual porque en un proyecto de 3000 líneas son la diferencia entre mantenible e infierno.

---

## 2. La indentación ES la sintaxis

No hay `{ }`. El bloque se define por sangría (4 espacios, siempre).

```python
if edad >= 18:
    print("mayor")
    print("sigue en el bloque")
print("fuera del bloque")
```

Un espacio de más es un error de sintaxis. Configurá el editor y olvidate.

---

## 3. Truthiness: esto te va a morder

En Python, muchas cosas "vacías" son falsas:

| Valor | Booleano |
|---|---|
| `0`, `0.0` | `False` |
| `""` | `False` |
| `[]`, `{}`, `set()`, `()` | `False` |
| `None` | `False` |
| Cualquier otra cosa | `True` |

Por eso el idioma pythónico para "si la lista tiene elementos" es:

```python
if items:            # ✅ pythónico
    ...

if len(items) > 0:   # ❌ funciona, pero te delata como recién llegado
    ...
```

---

## 4. `None` no es `null`, y se compara con `is`

`None` es un objeto único (un singleton). Siempre:

```python
if valor is None:        # ✅
if valor == None:        # ❌ funciona casi siempre, pero es incorrecto
```

`is` compara **identidad** (¿son el mismo objeto en memoria?).
`==` compara **valor** (¿tienen el mismo contenido?).

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b    # True  → mismo contenido
a is b    # False → objetos distintos
```

Regla práctica: usá `is` **solo** con `None`, `True` y `False`.

---

## 5. Mutabilidad — y la trampa clásica

| Mutable | Inmutable |
|---|---|
| `list`, `dict`, `set` | `str`, `int`, `float`, `tuple`, `bool` |

Los mutables se pasan por referencia, y esto genera **el bug número uno de los principiantes
en Python**:

```python
def agregar(item, carrito=[]):     # ☠️ NUNCA hagas esto
    carrito.append(item)
    return carrito

agregar("pan")    # ['pan']
agregar("leche")  # ['pan', 'leche']  ← ¡¿QUÉ?!
```

### La clave no es la mutabilidad, es CUÁNDO se evalúa el default

Viniendo de C# leés `carrito=[]` como *"si no me pasan carrito, creá una lista vacía"*,
o sea una instrucción que corre en cada llamada. **Python no hace eso.**

En Python `def` es una instrucción que **se ejecuta**. Cuando el intérprete llega a esa línea:

1. Evalúa `[]` → crea **un** objeto lista, una sola vez.
2. Crea la función y le guarda esa lista adentro, en `agregar.__defaults__`.
3. **Nunca más vuelve a evaluar ese `[]`.**

Cada llamada que no pasa `carrito` usa *ese mismo objeto*. `.append()` lo modifica en el
lugar, así que crece para siempre. Podés verlo:

```python
agregar.__defaults__    # ([],)  antes de llamarla
agregar("pan")
agregar.__defaults__    # (['pan'],)   ← el default se ensució
```

> Analogía con C#: es como si el `= new List<string>()` de un parámetro opcional fuera en
> realidad un `static readonly` de la clase. Una sola instancia, compartida por todas las
> llamadas, para siempre.

### La forma correcta

```python
def agregar(item, carrito=None):
    if carrito is None:
        carrito = []          # ← esta línea está en el CUERPO: corre en CADA llamada
    carrito.append(item)
    return carrito
```

El default sigue evaluándose una sola vez, pero es `None`: inmutable, no se puede ensuciar.

### ¿Por qué con un `int` no pasa?

```python
def sumar(n, total=0):
    total += n        # NO muta el 0: crea un int nuevo y reapunta la variable
    return total
```

Ese `0` también se crea una sola vez. Pero los `int` son inmutables, así que nadie puede
modificarlo. La regla completa es:

> **se evalúa una vez** + **se puede modificar en el lugar** = bug

Seguros como default: `int`, `str`, `float`, `bool`, `None`, `tuple`.
Peligrosos: `list`, `dict`, `set`.

### Dónde te va a pasar de verdad

```python
def crear_usuario(nombre: str, roles: list[str] = []):     # ☠️
def buscar(query: str, filtros: dict = {}):                # ☠️
def procesar(datos, vistos: set = set()):                  # ☠️
def registrar(evento: str, momento=datetime.now()):        # ☠️ el más traicionero
```

El último no tiene ninguna lista y falla igual: `datetime.now()` se congela cuando se
importa el módulo. Un servidor que corre tres días registra todos los eventos con la hora
del lunes.

**Corré `python leccion-01/demo_mutable_default.py`** para ver todo esto en vivo.

Memorizá el patrón `=None` + `if x is None`. Lo vas a usar toda tu vida en Python.

---

## 6. Slicing

Funciona en listas, strings, tuplas. Sintaxis: `secuencia[inicio:fin:paso]`.
El `fin` **no se incluye**.

```python
nums = [0, 1, 2, 3, 4, 5]

nums[1:4]     # [1, 2, 3]
nums[:3]      # [0, 1, 2]      desde el principio
nums[3:]      # [3, 4, 5]      hasta el final
nums[-1]      # 5              último elemento
nums[-2:]     # [4, 5]         últimos dos
nums[::-1]    # [5,4,3,2,1,0]  invertida
nums[::2]     # [0, 2, 4]      de dos en dos
```

Los índices negativos cuentan desde el final. Esto reemplaza un montón de `Substring()`
y `.slice()` con aritmética manual.

---

## 7. Desempaquetado (unpacking)

Podés asignar varias variables de una:

```python
a, b = 1, 2
a, b = b, a              # swap sin variable temporal

punto = (10, 20)
x, y = punto

primero, *resto = [1, 2, 3, 4]   # primero=1, resto=[2,3,4]
```

Y una función puede "devolver varios valores" (en realidad devuelve una tupla):

```python
def dividir(a: int, b: int) -> tuple[int, int]:
    return a // b, a % b

cociente, resto = dividir(17, 5)   # 3, 2
```

---

## 8. f-strings

La forma moderna de formatear. Prefijo `f` y llaves:

```python
nombre = "Ana"
total = 1234.5678

f"Hola {nombre}"                 # 'Hola Ana'
f"Total: {total:.2f}"            # 'Total: 1234.57'
f"{nombre.upper()} debe {total}" # podés meter expresiones adentro
f"{total=}"                      # 'total=1234.5678'  ← genial para debuggear
```

Olvidate de `%` y de `.format()`. Usá siempre f-strings.

---

## 9. Cosas que NO existen (y qué usar)

| En C#/JS | En Python |
|---|---|
| `i++` | `i += 1` |
| `cond ? a : b` | `a if cond else b` |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| `switch` | `match` (3.10+) o dict, o if/elif |
| `for (int i=0; i<n; i++)` | `for i in range(n)` |
| `null` | `None` |
| `true` / `false` | `True` / `False` |
| `//` comentario | `#` comentario |
| `x.Length` | `len(x)` |

El `for` de Python es **siempre** un `foreach`. Si necesitás el índice:

```python
for i, item in enumerate(items):
    print(i, item)
```

---

## 10. Entornos virtuales

El equivalente conceptual a `node_modules`, pero **no es automático**. Un venv es una carpeta
con una copia aislada de Python y sus paquetes, para que un proyecto no le pise las
dependencias a otro.

```powershell
python -m venv .venv              # crear
.\.venv\Scripts\Activate.ps1      # activar (Windows PowerShell)
pip install pytest                # instalar dentro del venv
pip freeze > requirements.txt     # congelar versiones
deactivate                        # salir
```

Sabés que está activo porque el prompt muestra `(.venv)` adelante.

**Regla:** un venv por proyecto, siempre, desde el día uno. Nunca instales con `pip`
sin tener un venv activo.

---

## Ahora sí

1. Abrí `ejercicios.py`
2. Completá cada función (reemplazá el `...` por tu código)
3. Corré: `pytest leccion-01 -v`
4. Cuando pasen los 10, avisame y te reviso el código.

No mires los tests para "adivinar" la respuesta más de lo necesario — están ahí para
decirte si funciona, no para dictarte la solución.
