# Lección 05 — Decoradores

Duración: ~20 min de lectura + 40 min de ejercicios.

En la lección 04, el ejercicio 10 te quedó así:

```python
def contar_llamadas(func):
    def envoltorio(*args, **kwargs):
        envoltorio.llamadas += 1
        return func(*args, **kwargs)

    envoltorio.llamadas = 0
    return envoltorio
```

Eso **ya es un decorador**. Toda esta lección es aprender a usarlo bien y a leerlo
cuando lo escribió otro.

---

## 1. `@` es azúcar sintáctica. Nada más.

Estas dos cosas son exactamente lo mismo:

```python
def saludar(nombre):
    return f"Hola, {nombre}"


saludar = contar_llamadas(saludar)  # ← la forma larga
```

```python
@contar_llamadas  # ← la forma corta
def saludar(nombre):
    return f"Hola, {nombre}"
```

El `@` significa: **"tomá la función que definí abajo, pasásela a esto, y guardá el
resultado con el mismo nombre"**. Se aplica una sola vez, en el momento en que Python lee
el `def` — no en cada llamada.

Cuando dudes de qué hace un decorador, reescribilo mentalmente en la forma larga.

### Esto no es un atributo de C#

Un `[Obsolete]` o un `[HttpGet]` de C# son **metadata**: quedan pegados al método y no
hacen nada hasta que alguien los lee por reflexión. Un decorador de Python **reemplaza la
función**. Después de `@contar_llamadas`, el nombre `saludar` ya no apunta a lo que
escribiste: apunta a `envoltorio`.

Esa es toda la diferencia, y explica el 90% de las sorpresas con decoradores.

---

## 2. El decorador mínimo

Un decorador es una función que **recibe una función y devuelve una función**.

```python
def anunciar(func):
    def envoltorio(*args, **kwargs):
        print(f"-> entrando a {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"<- saliendo de {func.__name__}")
        return resultado

    return envoltorio
```

Las tres cosas que casi siempre querés adentro del envoltorio:

1. `*args, **kwargs` en la firma → **acepta cualquier función**
2. `func(*args, **kwargs)` → le pasa todo tal cual
3. `return resultado` → **devolvé lo que devuelva la original**

El punto 3 es el error más común: si te olvidás el `return`, tu función decorada devuelve
`None` y el bug aparece lejos de acá.

---

## 3. El problema: el decorador pisa la identidad

```python
@anunciar
def saludar(nombre):
    """Saluda a alguien."""
    return f"Hola, {nombre}"


saludar.__name__  # 'envoltorio'   ❌
saludar.__doc__  # None            ❌
```

Claro: `saludar` **es** `envoltorio` ahora. Perdiste el nombre, el docstring y la firma.

Eso no es cosmético. `pytest` descubre tests por nombre, FastAPI arma la documentación
leyendo la firma, y cualquier traceback te va a decir `envoltorio` en vez de la función
real. Un decorador sin esto arriba rompe herramientas.

### `functools.wraps` — la línea que nunca hay que olvidar

```python
from functools import wraps


def anunciar(func):
    @wraps(func)  # ← copia __name__, __doc__, __module__, etc. de func al envoltorio
    def envoltorio(*args, **kwargs):
        return func(*args, **kwargs)

    return envoltorio
```

Ahora `saludar.__name__` vuelve a ser `'saludar'`.

`wraps` es a su vez un decorador con parámetros (sección 4) — por eso lleva paréntesis:
`@wraps(func)`, no `@wraps`.

> **Regla:** todo decorador que devuelva un envoltorio lleva `@wraps(func)`. Sin
> excepciones. Si no envuelve (sección 6), no hace falta.

---

## 4. Decoradores con parámetros: la capa de más

Esto es lo que confunde a todo el mundo la primera vez. Compará las dos formas de usarlo:

```python
@anunciar  # sin paréntesis
def f(): ...


@prefijo("LOG: ")  # CON paréntesis
def g(): ...
```

Desazucará el segundo y se entiende solo:

```python
g = prefijo("LOG: ")(g)
#   └────┬────────┘└┬┘
#        │          └── esto es la llamada del decorador de siempre
#        └── así que prefijo("LOG: ") tiene que DEVOLVER un decorador
```

O sea: `prefijo` no es el decorador. `prefijo` es una **fábrica de decoradores**. Por eso
hay tres niveles:

```python
def prefijo(texto):  # 1) recibe los PARÁMETROS
    def decorador(func):  # 2) recibe la FUNCIÓN
        @wraps(func)
        def envoltorio(*args, **kwargs):  # 3) recibe los ARGUMENTOS de la llamada
            return texto + func(*args, **kwargs)

        return envoltorio

    return decorador
```

Leído de afuera hacia adentro: parámetros → función → argumentos. Cada nivel devuelve el
de abajo.

Es el mismo closure de la lección 04, dos veces anidado. `texto` sigue vivo adentro de
`envoltorio` por la misma razón que `saludo` seguía vivo adentro de `saludar`.

⚠️ El error clásico: `@prefijo` sin paréntesis cuando el decorador lleva parámetros. Ahí
`func` termina valiendo lo que debería ser `texto`, y el mensaje de error no se entiende
nada. Si un decorador tiene parámetros, **siempre** va con paréntesis.

---

## 5. Apilar decoradores

```python
@negrita
@cursiva
def texto():
    return "hola"
```

Se aplican **de abajo hacia arriba** — el más cercano al `def` primero:

```python
texto = negrita(cursiva(texto))
```

Al ejecutar, en cambio, el de arriba es el que corre primero (es el de más afuera). Si
`negrita` agrega `**` y `cursiva` agrega `_`, el resultado es `**_hola_**`.

**Truco para acordarte:** se apilan como paréntesis. El de abajo queda adentro.

Cuando el orden cambia el resultado, importa mucho. Un `@validar` afuera de un `@cachear`
valida siempre; adentro, se saltea la validación en los hits de caché.

---

## 6. Un decorador no está obligado a envolver

Puede devolver la función **tal cual** y aprovechar el momento en que se aplica para hacer
otra cosa. El caso típico es un **registro**:

```python
COMANDOS = {}


def comando(nombre):
    def decorador(func):
        COMANDOS[nombre] = func  # el efecto: anotarla en el registro
        return func  # y la devuelvo intacta

    return decorador


@comando("saludar")
def saludar_usuario():
    return "hola!"
```

`saludar_usuario` sigue siendo exactamente la función que escribiste — no hay envoltorio,
no hace falta `wraps`. Lo único que pasó es que, al importarse el módulo, quedó anotada en
`COMANDOS`.

Así funcionan `@app.route("/")` de Flask, `@app.get("/items")` de FastAPI y
`@pytest.fixture`. No envuelven tu función: la registran en una tabla que el framework
recorre después. Es el dispatch table de la lección 04, llenado de forma declarativa.

---

## 7. `functools.cache` — memoización gratis

```python
from functools import cache


@cache
def consultar_precio(producto):
    print(f"consultando {producto}...")  # solo se imprime la primera vez
    return len(producto) * 100


consultar_precio("teclado")  # consulta
consultar_precio("teclado")  # devuelve lo guardado, no vuelve a entrar
```

`@cache` guarda un dict interno `{argumentos: resultado}`. Si ya vio esos argumentos,
devuelve lo de antes sin ejecutar el cuerpo.

Trae un par de extras:

```python
consultar_precio.cache_info()  # CacheInfo(hits=1, misses=1, maxsize=None, currsize=1)
consultar_precio.cache_clear()  # vaciar
```

Dos condiciones y una advertencia:

- **Los argumentos tienen que ser hashables** — se usan como clave de un dict. Un `str`,
  `int` o `tuple` sirven; una `list` o un `dict` revientan con `TypeError`.
- **La función tiene que ser pura**: mismos argumentos, mismo resultado. Cachear algo que
  lee la hora o la base de datos te va a dar respuestas viejas.
- **El caché no se vacía nunca.** Si los argumentos posibles son infinitos, es un memory
  leak. Para eso está `@lru_cache(maxsize=128)`, que descarta los menos usados.

`@cache` (Python 3.9+) es literalmente `@lru_cache(maxsize=None)` con mejor nombre.

---

## 8. `raise` — lo mínimo para validar

Los ejercicios necesitan cortar la ejecución cuando algo está mal:

```python
if not texto.strip():
    raise ValueError("el texto no puede estar vacío")
```

`raise` corta ahí mismo: no ejecuta nada de lo que sigue y propaga el error hacia arriba.
Es el `throw new ArgumentException(...)` de C#.

Las que vas a usar por ahora:

- `ValueError` — el tipo es el correcto pero el valor no sirve (un string vacío, un
  negativo donde no va)
- `TypeError` — el tipo directamente no es el que corresponde

**Atraparlos es la Fase 4.** Por ahora solo los lanzás. En los tests vas a ver esto, que
es "esto tiene que fallar así":

```python
with pytest.raises(ValueError):
    saludar("")
```

---

## Antes de arrancar

Corré `python leccion-05/demo_decoradores.py`. Muestra el desazucarado, el `__name__`
pisado, y el orden de apilado — las tres cosas que se entienden mucho mejor viéndolas.

1. `python leccion-05/demo_decoradores.py`
2. Abrí `ejercicios_05.py`
3. `pytest leccion-05 -v`
4. `ruff format leccion-05` y `ruff check leccion-05` **antes** de mostrármelo (la vez
   pasada te lo salteaste)

Los ejercicios 7 y 8 van de a pares: primero escribís el caché a mano, después lo
reemplazás por `@cache` y ves cuánto código desaparece. El 10 hace lo mismo con el
ejercicio 1.
