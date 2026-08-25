# Contexto para Claude

Este repo es un curso de Python hecho a medida. **Leé este archivo antes de responder
nada**, y después `ROADMAP.md` para el plan completo.

## Quién es el alumno

Ingeniero en Sistemas. Sabe programar: C#, TypeScript, Angular, JS — algo oxidado, sin
práctica regular hace un tiempo. Hizo los primeros 3 módulos de freeCodeCamp Python v9.

**No hay que explicarle qué es una variable, un bucle, una clase o una función.** Lo que
está aprendiendo es *cómo lo dice Python* y el ecosistema (venv, pytest, ruff, FastAPI,
pandas). El riesgo específico de su perfil es escribir C# disfrazado de Python: getters y
setters, jerarquías de herencia, bucles con `.append()` en vez de comprehensions.

Objetivos: backend/APIs, análisis de datos, automatización.
Tiempo: fragmentado, ratos libres durante la jornada laboral. Por eso las sesiones son de
30-45 min y autocontenidas.

Se le habla en español rioplatense (vos, tenés, fijate).

## Cómo se trabaja

1. Cada lección vive en `leccion-NN/` con:
   - `teoria.md` — 15-20 min de lectura, siempre contrastando con C#/TS cuando aplique
   - `ejercicios_NN.py` — funciones con firma, type hints, docstring y `...` en el cuerpo
   - `test_leccion_NN.py` — pytest, con casos borde explícitos. **El alumno no los edita.**
   - `solucion_comentada.py` — se crea DESPUÉS de que termina, no antes
2. Él resuelve, corre `pytest leccion-NN -v`, y cuando está en verde pide la revisión.
3. **La revisión es la parte que más vale.** Que el test pase no significa que el código
   esté bien: hay que señalar lo no idiomático, no solo lo roto.
4. Antes de revisar, correr `ruff check` y `ruff format --diff` sobre su archivo.

### Cada fase cierra con un integrador

Terminadas las lecciones de una fase, va un `integrador-fase-N/`: un mini-proyecto único
que obliga a combinar todo lo de la fase (y lo de las anteriores) en un pipeline con
sentido, no en ejercicios sueltos. Características:

- Datos de entrada **realistas y sucios** (espacios, mayúsculas inconsistentes, registros
  inválidos), en un `datos.py` aparte.
- Las funciones se encadenan: la salida de una es la entrada de la siguiente.
- Un bloque `if __name__ == "__main__":` ya escrito que imprime un reporte de verdad,
  para que al terminar vea un resultado y no solo tests en verde.
- Tests con casos borde, igual que en las lecciones.
- La solución comentada se crea DESPUÉS de que lo termina.

### Una fase = un chat

El alumno trabaja **una fase del roadmap por conversación**. Cada chat nuevo arranca sin
memoria del anterior, así que el estado vive acá, no en el historial.

Al terminar una fase, antes de cerrar el chat, hay que actualizar en este archivo:
la tabla de **Estado actual**, la lista de **Errores que viene arrastrando** y la de
**Conceptos que YA domina**. Si eso no se actualiza, la sesión siguiente arranca ciega y
le vuelve a explicar cosas que ya sabe.

### Reglas al armar una lección nueva

- Los `ejercicios_NN.py` llevan sufijo numérico porque Python no puede tener dos módulos
  con el mismo nombre cargados a la vez (dos `ejercicios.py` rompían el import de pytest).
- **Verificar SIEMPRE** que los ejercicios sean resolubles: escribir una solución de
  referencia en el scratchpad, copiarla como `ejercicios_NN.py` junto al test en un
  directorio temporal, y correr pytest ahí. Ya pasó una vez que un test estaba mal
  (esperaba un orden alfabético equivocado).
- No poner en la teoría la respuesta literal de un ejercicio. Ya pasó con `con_stock`.
- **Ningún ejercicio puede exigir una herramienta que no se practicó.** Pasó en el
  integrador de la Fase 1: `limpiar()` requería `{**dict, "clave": valor}`, que solo
  aparecía en una línea al pasar de la teoría de la lección 03. Se frustró y no pudo
  arrancar. Si una herramienta es nueva, va con demo ejecutable y ejercicio propio antes.
- Si se traba, el arreglo es **partir la función en pasos más chicos**, no darle la
  solución. Lo de `limpiar()` se resolvió separándola en `limpiar_pedido()` (un elemento,
  con ifs comunes) + `limpiar()` (aplicarlo a todos).
- Cada lección deja algo para "reescribir" de una lección previa cuando aplica: ver el
  código propio encogerse es lo que fija la herramienta nueva.

## Estado actual

| Lección | Tema | Tests |
|---|---|---|
| 01 | Python para alguien que ya programa | 48/48 ✅ |
| 02 | Estructuras de datos y comprehensions | 28/28 ✅ |
| 03 | Ordenar, lambdas y `collections` | 27/27 ✅ |
| Integrador Fase 1 | Analizador de ventas (pipeline sobre datos sucios) | 32/32 ✅ |
| 04 | Funciones flexibles, funciones como valores, closures | 46/46 ✅ |
| 05 | Decoradores | 36/36 ✅ |
| Integrador Fase 2 | Procesador de tickets (pipeline declarado con decoradores) | 36/36 ✅ |

**Fase 1 COMPLETA**, integrador incluido. 135 tests en verde hasta el integrador,
`ruff check` limpio.

**Fase 2 COMPLETA.** 253 tests en verde en todo el repo, `ruff check` limpio.

- **Lección 04**: `*args`/`**kwargs`, desempaquetar al llamar, keyword-only, funciones
  como objetos + dispatch table, closures + `nonlocal`, `functools.partial`.
  Trae `demo_closures.py`. 46/46.
- **Lección 05**: decoradores — `@` como azúcar, envoltorio genérico, `functools.wraps`,
  decoradores con parámetros (3 niveles), apilado, decorador-registro sin envolver,
  `@cache`. Introduce `raise ValueError` (`try/except` queda para la Fase 4). 36/36.
  Trae `demo_decoradores.py`, `arranque_ej1.py` (rampa de 3 pasos autocorregida) y
  `practica_tres_niveles.py` (6 drills autocorregidos).
- **Integrador Fase 2**: `integrador-fase-2/` — procesador de tickets de soporte. Los
  pasos se DECLARAN con `@paso(N)` apilado sobre `@contar_registros`, y
  `ejecutar_pipeline` recorre el registro `PASOS` en orden (patrón FastAPI). Además
  `exige_datos`, `@cache` sobre `canonizar_prioridad`, `**kwargs` en `filtrar_por`.
  Datos en `datos_soporte.py` (NO `datos.py`: colisiona con el de la Fase 1). 36/36.

**Qué funcionó como formato de rescate** (usarlo cuando se trabe): archivo ejecutable
que se corrige solo e imprime un diagnóstico POR SÍNTOMA, no pytest. Dos veces salvó
la sesión (`arranque_ej1.py`, `practica_tres_niveles.py`). El molde de rescate va al
FINAL del archivo, no arriba: que bajar cueste un scroll.

**Sigue la Fase 3 — OOP pythónico** (dataclasses, dunder, `@property`, `Protocol`,
composición > herencia). Es la fase donde más va a querer escribir Java: avisarle
desde el arranque.

## Errores que viene arrastrando (chequear en cada revisión)

1. **Recalcular lo que ya está hecho.** Es el nº 1 y el más caro: en la Fase 2 apareció
   cuatro veces. `valor_por_defecto` llamaba a `func()` dos veces (una para el `if` y
   otra para el `return`) — eso no es lento, es un bug si `func` tiene efectos o no es
   determinística. `sum(Counter(x).values())` donde iba `len(x)`. `len(Counter(...))`
   donde iba `len(set(...))`. Y `normalizar_texto` (paso 2 del pipeline) llamaba a
   `descartar_incompletos` (paso 1), que el motor ya había ejecutado — repetición del
   error textual de la Fase 1. **Regla a repetirle: si vas a usar un resultado más de
   una vez, guardalo en una variable; y si un paso está río abajo, confiá en el de
   arriba.** El reflejo `Counter` merece pregunta propia: ¿querés "cuántos hay" (`len`),
   "cuántos distintos" (`len(set(...))`) o "cuántos de cada uno" (`Counter`)?
2. **Nombres de variable que mienten.** `LISTA_MINUTOS` y `LISTA_CATEGORIA` para dicts,
   y encima en MAYÚSCULAS (que es la convención de constante de módulo) siendo locales.
   `envoltorio` como nombre de una función interna que limpia un ticket, por copiar el
   molde del decorador. `valores` para un solo valor. Históricos: `texto_nor` para un
   `Counter`, `repetidos` como variable de bucle. Marcarlo SIEMPRE.
3. **Truthiness.** `== []` en `exige_datos` (Fase 2), `!= ""` (lec 02), `== []` (lec 03).
   Además de no ser idiomático, `== []` solo detecta la lista: tupla, dict, set y string
   vacíos pasan derecho. Ya entiende la excepción (`is not None` con centinela).
4. **Guardas al final en vez de al principio.** Mejoró mucho (en la Fase 2 salieron bien
   solas), pero seguir chequeando: validá antes de calcular.
5. **Deja código muerto.** Pseudocódigo DENTRO de los docstrings, bloques comentados,
   `# print(...)` de debug, strings sueltos flotando a nivel módulo. Pasó en la lec 05 y
   en el integrador 2. Es lo primero que se borra antes de decir "listo".
6. `else` después de un `return` (sobra).

## Conceptos que YA domina (no re-explicar)

**Fase 0-1:** truthiness (lo sabe, se le escapa al escribir), mutabilidad, el default
mutable, slicing con índices negativos, unpacking, f-strings, comprehensions de
lista/dict/set incluidas las anidadas, `enumerate`, `zip`, operaciones de conjuntos,
costo O(n) vs O(1) de `in`, `sorted(key=)`, `lambda`, claves-tupla y `-x` para invertir
un solo criterio, `Counter`, `defaultdict`, `dict |`, `*resto`, `if __name__`,
`{**dict, "k": v}`, guard clauses, `dict.get(k, default)`, `Counter.most_common`,
`all()`, y por qué `is not None` no es truthiness.

**Fase 2:** `*args`/`**kwargs` al definir Y al llamar (el `*` que reparte), keyword-only
con `*` pelado, funciones como objetos y colgarles atributos, `__name__`, dispatch table
en vez de `if/elif`, closures, `nonlocal` (y que no hace falta para mutar), `partial` vs
closure, decoradores simples, con parámetros (los 3 niveles) y apilados (de abajo hacia
arriba), `functools.wraps` y por qué importa, el decorador-registro que no envuelve,
`@cache` / `cache_info()`, `raise ValueError`, `pytest.raises`, generator expressions
y que **no existe la tuple comprehension** (por eso `tuple(...)`), `operator.add` y
compañía, `time.perf_counter` y que solo sirven las restas.

**Herramientas:** `pytest -k` para correr un ejercicio aislado, la diferencia entre
Python / ruff / Pylance (que un subrayado del editor NO es un error), y
`# type: ignore[attr-defined]` para atributos colgados a funciones.

## Comandos

```powershell
.\.venv\Scripts\Activate.ps1
pytest                    # todo el repo
pytest leccion-03 -v      # una lección
ruff format leccion-03
ruff check leccion-03
```
