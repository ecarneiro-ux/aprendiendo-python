# Roadmap: de "sé programar" a Python intermedio

**Punto de partida:** Ing. en Sistemas con base en C#, TypeScript, Angular y JS (algo oxidada) +
3 módulos de freeCodeCamp Python v9.

**Objetivo:** Backend/APIs, análisis de datos y automatización.

**Formato:** sesiones de 30-45 min autocontenidas. Podés hacer una por día o tres seguidas
un domingo. Cada lección tiene teoría corta, ejercicios con tests, y se corrige sola.

**Regla de oro:** si en una sesión no escribiste código que corriera, esa sesión no cuenta.

---

## Fase 0 — Python para alguien que ya programa (1-2 sesiones)

Lo que Python hace distinto a C#/TS y te va a morder si no lo sabés.

- Tipado dinámico + type hints (opcionales, pero los vamos a usar siempre)
- Indentación como sintaxis
- Truthiness: `[]`, `""`, `0`, `None` son falsos
- `None` vs `null`, y por qué se compara con `is`
- Mutabilidad: `list`/`dict`/`set` vs `tuple`/`str` — y la trampa del argumento por defecto mutable
- Slicing, unpacking, f-strings
- `==` vs `is`
- `venv` y `pip` (el equivalente a NuGet / node_modules, pero con menos magia)

> **Lección 01** ← empezá acá

## Fase 1 — Estructuras de datos e idiomática (3-4 sesiones)

Acá es donde tu código deja de parecer C#.

- `list`, `dict`, `set`, `tuple`: cuándo cada uno
- Comprehensions (`[x for x in ...]`) — reemplazan el 80% de tus `for` con `.push()`
- `enumerate`, `zip`, `sorted` con `key=`
- `collections`: `Counter`, `defaultdict`, `deque`
- Desempaquetado avanzado: `*args`, `a, *resto = lista`

> **Integrador Fase 1** — `integrador-fase-1/`: analizador de ventas sobre datos sucios.

## Fase 2 — Funciones de verdad (2-3 sesiones)

- `*args` / `**kwargs`
- Funciones como valores de primera clase (esto ya lo sabés de JS)
- Closures
- Decoradores (el equivalente conceptual a los atributos/annotations de C#, pero ejecutables)
- `functools`: `wraps`, `lru_cache`, `partial`

## Fase 3 — OOP pythónico (3 sesiones)

Ojo acá: venís de C# y vas a querer escribir Java. Python es más liviano.

- Clases, `self`, atributos de clase vs de instancia
- `dataclasses` (tu nuevo mejor amigo, reemplaza los DTOs con boilerplate)
- Dunder methods: `__repr__`, `__eq__`, `__len__`, `__iter__`
- `@property` en vez de getters/setters
- Duck typing y `Protocol` en vez de interfaces
- Composición > herencia

## Fase 4 — Errores y context managers (2 sesiones)

- Jerarquía de excepciones, excepciones propias
- `try/except/else/finally`
- `with` y cómo escribir tu propio context manager
- `logging` (dejá de usar `print` para diagnosticar)

## Fase 5 — Iteradores y generadores (2 sesiones)

Concepto que no tiene equivalente directo cómodo en C# viejo, y es central en Python.

- El protocolo de iteración
- `yield` y funciones generadoras
- Evaluación perezosa: procesar un archivo de 10 GB sin cargarlo en RAM
- `itertools`

## Fase 6 — Calidad y proyecto real (3 sesiones)

- Estructura de un proyecto Python (`src/`, `pyproject.toml`, paquetes)
- `pytest`: fixtures, parametrize
- Type hints en serio + `mypy`
- `ruff` (linter + formateador, rapidísimo)
- Debugging con `pdb` y con VS Code

## Fase 7 — Backend / APIs (3-4 sesiones)

- FastAPI: endpoints, validación con Pydantic, inyección de dependencias
- Async/await (te va a resultar familiar de TS, pero con diferencias importantes)
- SQL con SQLAlchemy o SQLModel
- Testear una API

## Fase 8 — Datos y análisis (3-4 sesiones)

- `pandas`: DataFrame, filtrado, groupby, merge
- Leer CSV/JSON/Excel/SQL
- Gráficos con matplotlib
- Notebooks: cuándo sí y cuándo no

## Fase 9 — Automatización (2 sesiones)

- `pathlib`, `os`, `shutil`
- `requests` / `httpx` contra APIs externas
- `argparse` o `typer` para CLIs
- Tareas programadas

---

## Estimación honesta

~25-30 sesiones de 45 min ≈ **20 horas de trabajo efectivo**.

- 3 sesiones/semana → **~10 semanas**
- 1 sesión/semana → ~7 meses (funciona, pero vas a olvidar cosas entre medio)

El mínimo que recomiendo: **2 sesiones por semana**. Por debajo de eso, el olvido
le gana al avance.

## Cómo trabajamos

1. Abrís la lección, leés la teoría (10 min).
2. Completás `ejercicios.py`. **No mires la solución.**
3. Corrés los tests: `pytest leccion-01 -v`
4. Cuando algo falla, me preguntás. No te quedes trabado más de 15 min.
5. Cuando pasan todos, te reviso el código y te muestro cómo lo escribiría un pythonista.

El paso 5 es el que más vale. Que el test pase no significa que el código esté bien.
