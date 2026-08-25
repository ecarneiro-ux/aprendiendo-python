"""
Integrador de la Fase 2 — Procesador de tickets de soporte.

Te llega la exportación cruda de un sistema de tickets. Hay que limpiarla y
sacar un reporte, igual que en la Fase 1. La diferencia es CÓMO se arma el
pipeline: acá los pasos no se llaman a mano uno atrás de otro. Cada paso se
declara con un decorador que lo anota en un registro, y `ejecutar_pipeline`
recorre ese registro en orden.

Es como funciona un framework de verdad: vos declarás, el motor ejecuta.

    Parte A (1-4)   la infraestructura: los decoradores y el motor
    Parte B (5-8)   los pasos del pipeline, declarados con @paso
    Parte C (9-12)  el análisis sobre los datos ya limpios

La Parte A hay que hacerla primero: sin ella, la B no se puede ni declarar.

Cuando esté todo, corré:
    python integrador-fase-2/pipeline.py
y vas a ver el reporte, con las métricas que juntaron tus propios decoradores.

Herramientas de las fases 1 y 2: comprehensions, Counter/defaultdict,
sorted(key=), *args/**kwargs, closures, decoradores simples y con parámetros,
apilado, wraps, cache, raise ValueError, dispatch tables.
"""

import sys

# Están los dos a mano; probablemente uses uno solo.
# Si al final te sobra alguno, borralo: ruff te lo va a marcar como F401.
from collections import defaultdict
from collections.abc import Callable
from functools import cache, wraps

from datos_soporte import TICKETS_CRUDOS

# ===========================================================================
# PARTE A — La infraestructura
# ===========================================================================

# Acá se van a ir anotando los pasos del pipeline: {orden: función}
PASOS: dict[int, Callable] = {}


# ---------------------------------------------------------------------------
# 1. El decorador que mide cuánto filtra cada paso
# ---------------------------------------------------------------------------
def contar_registros(func):
    """Decorador para un paso del pipeline: guarda cuántos tickets entraron y
    cuántos salieron en la ÚLTIMA corrida.

    Un paso del pipeline recibe una lista de tickets como primer argumento
    posicional y devuelve otra lista.

    Requisitos:
      - `.entraron` y `.salieron` en el envoltorio, ambos arrancan en 0
      - devuelve lo que devuelva `func`, sin tocarlo
      - `@wraps(func)`, como siempre

    Es el `contar_llamadas` de la lección 04 con otra cuenta.

    >>> @contar_registros
    ... def sacar_pares(numeros):
    ...     return [n for n in numeros if n % 2]
    >>> sacar_pares([1, 2, 3, 4])
    [1, 3]
    >>> sacar_pares.entraron, sacar_pares.salieron
    (4, 2)
    """

    @wraps(func)
    def envoltorio(*args, **kwargs):
        envoltorio.entraron = len(args[0])  # type: ignore[attr-defined]
        resultado = func(*args, **kwargs)
        envoltorio.salieron = len(resultado)  # type: ignore[attr-defined]
        return resultado

    envoltorio.entraron = 0  # type: ignore[attr-defined]
    envoltorio.salieron = 0  # type: ignore[attr-defined]
    return envoltorio


# ---------------------------------------------------------------------------
# 2. El decorador que declara un paso del pipeline
# ---------------------------------------------------------------------------
def paso(orden: int):
    """Fábrica de decoradores: anota `func` en PASOS bajo la clave `orden` y la
    devuelve INTACTA.

    No envuelve nada: el efecto pasa al decorar, no al llamar. Es el mismo
    patrón que `@app.get("/ruta")` de FastAPI.

    Ojo con el apilado, más abajo:

        @paso(1)
        @contar_registros
        def descartar_incompletos(tickets): ...

    `@contar_registros` es el de abajo, así que se aplica primero; `@paso(1)`
    recibe el envoltorio que salió de ahí y ES ESE el que queda registrado.
    Si el orden fuera al revés, en PASOS quedaría la función sin instrumentar
    y las métricas del reporte saldrían en cero.
    """

    def decorador(func):
        PASOS[orden] = func
        return func

    return decorador


# ---------------------------------------------------------------------------
# 3. El motor
# ---------------------------------------------------------------------------
def ejecutar_pipeline(tickets: list[dict]) -> list[dict]:
    """Aplica todos los pasos de PASOS, de menor a mayor orden, encadenados: la
    salida de cada uno es la entrada del siguiente.

    No hardcodees los nombres de los pasos. La gracia es que agregar un paso
    nuevo sea escribir un `@paso(4)` y nada más.

    Con PASOS vacío, devolvé la lista tal cual.
    """
    resultado = tickets

    for orden in sorted(PASOS):
        funcion_actual = PASOS[orden]

        resultado = funcion_actual(resultado)
    return resultado


# ---------------------------------------------------------------------------
# 4. El decorador que valida antes de calcular
# ---------------------------------------------------------------------------
def exige_datos(func):
    """Decorador: si el primer argumento posicional es una colección vacía,
    lanzá `ValueError` sin llamar a `func`.

    Esto es la guarda del `resumen()` del integrador de la Fase 1, la que se te
    escapó y reventó con ZeroDivisionError. Ahora en vez de acordarte de
    escribirla en cada función, la ponés una vez y la pegás con un `@`.

    `@wraps(func)`, como siempre.
    """

    @wraps(func)
    def envoltorio(*args, **kwargs):
        if not args[0]:
            raise ValueError("El primer argumento no puede ser una coleccion vacia")
        return func(*args, **kwargs)

    return envoltorio


# ===========================================================================
# PARTE B — Los pasos del pipeline
# ===========================================================================
# Los tres van decorados así, y en este orden:
#
#     @paso(N)
#     @contar_registros
#     def ...
#
# Los decoradores hay que agregarlos vos: las firmas están, los @ no.


# ---------------------------------------------------------------------------
# 5. Paso 1 — tirar la basura
# ---------------------------------------------------------------------------
@paso(1)
@contar_registros
def descartar_incompletos(tickets: list[dict]) -> list[dict]:
    """Devuelve solo los tickets utilizables.

    Un ticket es inútil si el usuario está vacío o son puros espacios, o si los
    minutos no son mayores a 0.

    Ojo: acá los datos todavía vienen crudos, así que "   " tiene que contar
    como vacío. La lista original no se toca.

    Este es el primer paso a propósito: los pasos que siguen dan por hecho que
    ya no hay basura.
        "id": 101,
        "usuario": "  ana perez ",
        "categoria": " Redes ",
        "prioridad": "ALTA",
        "minutos": 45,
    """
    return [
        tick for tick in tickets if (tick["usuario"].strip() and tick["minutos"] > 0)
    ]


# ---------------------------------------------------------------------------
# 6. Paso 2 — emparejar el texto
# ---------------------------------------------------------------------------
@paso(2)
@contar_registros
def normalizar_texto(tickets: list[dict]) -> list[dict]:
    """Devuelve los tickets con `usuario` y `categoria` emparejados:

        usuario   -> sin espacios en los extremos, iniciales en mayúscula
                     "  ana perez " -> "Ana Perez"
        categoria -> sin espacios en los extremos, todo en minúscula
                     " Redes "      -> "redes"

    El resto de las claves se copian tal cual. Los dicts originales NO se
    modifican: acordate de `{**ticket, "clave": valor}`.
    """

    return [
        {
            **ticket,
            "usuario": ticket["usuario"].strip().title(),
            "categoria": ticket["categoria"].strip().lower(),
        }
        for ticket in tickets
    ]


# ---------------------------------------------------------------------------
# 7. La tabla de prioridades (con caché)
# ---------------------------------------------------------------------------
PRIORIDADES = {
    "alta": "alta",
    "a": "alta",
    "high": "alta",
    "media": "media",
    "m": "media",
    "normal": "media",
    "baja": "baja",
    "b": "baja",
    "low": "baja",
}


@cache
def canonizar_prioridad(texto: str) -> str:
    """Convierte cómo vino escrita la prioridad a una de: "alta", "media", "baja".

    Ignorá espacios y mayúsculas. Si no está en la tabla PRIORIDADES (o vino
    vacía), devolvé "media".

    Dos cosas para resolverlo:
      - la tabla ya está: esto es una búsqueda con valor por defecto, no una
        cadena de ifs
      - agregale el decorador de `functools` que evita recalcular lo mismo:
        hay más tickets que formas distintas de escribir la prioridad, así que
        varios argumentos se repiten. El reporte imprime los hits del caché.
        Hay un test que verifica que esté.

    >>> canonizar_prioridad("  ALTA ")
    'alta'
    >>> canonizar_prioridad("urgentísimo")
    'media'
    """

    return PRIORIDADES.get(texto.strip().lower(), "media")


# ---------------------------------------------------------------------------
# 8. Paso 3 — aplicar la tabla
# ---------------------------------------------------------------------------
@paso(3)
@contar_registros
def unificar_prioridad(tickets: list[dict]) -> list[dict]:
    """Devuelve los tickets con la prioridad ya canonizada.

    Usá `canonizar_prioridad`. Sin modificar los originales.
    """
    return [
        {**ticket, "prioridad": canonizar_prioridad(ticket["prioridad"])}
        for ticket in tickets
    ]


# ===========================================================================
# PARTE C — El análisis, sobre los datos ya limpios
# ===========================================================================


# ---------------------------------------------------------------------------
# 9. El resumen
# ---------------------------------------------------------------------------
@exige_datos
def resumen(tickets: list[dict]) -> dict:
    """Devuelve las cifras generales:

        {"tickets": 3, "minutos": 90, "promedio": 30.0, "usuarios": 2}

      tickets   cuántos hay
      minutos   la suma de todos
      promedio  minutos / tickets, redondeado a 2 decimales
      usuarios  cuántos usuarios DISTINTOS

    Con la lista vacía tiene que lanzar ValueError. No escribas el if: para eso
    hiciste el ejercicio 4.
    """
    tickets_cant = len(tickets)
    minutos_suma = sum(ticket["minutos"] for ticket in tickets)
    promedio_tick = round(minutos_suma / tickets_cant, 2)
    usuarios = len({t["usuario"] for t in tickets})
    return {
        "tickets": tickets_cant,
        "minutos": minutos_suma,
        "promedio": promedio_tick,
        "usuarios": usuarios,
    }


# ---------------------------------------------------------------------------
# 10. Minutos por usuario
# ---------------------------------------------------------------------------
def minutos_por_usuario(tickets: list[dict]) -> dict[str, int]:
    """Devuelve {usuario: minutos totales}.

    Devolvé un dict común, no un defaultdict.
    """
    minutos_acumulados = defaultdict(int)
    for tic in tickets:
        minutos_acumulados[tic["usuario"]] += tic["minutos"]
    return dict(minutos_acumulados)


# ---------------------------------------------------------------------------
# 11. Ranking de categorías
# ---------------------------------------------------------------------------
def ranking_categorias(tickets: list[dict]) -> list[tuple[str, int]]:
    """Devuelve [(categoria, minutos)] de mayor a menor cantidad de minutos.
    Si dos empatan, van en orden alfabético.

    Los dos criterios van en direcciones opuestas: releé lo de la clave-tupla
    de la lección 03 si hace falta.
    """
    acumulado = defaultdict(int)
    for tic in tickets:
        acumulado[tic["categoria"]] += tic["minutos"]
    return sorted(
        dict(acumulado).items(),
        key=lambda par: (-par[1], par[0]),
    )


# ---------------------------------------------------------------------------
# 12. Filtrar por lo que sea
# ---------------------------------------------------------------------------
def filtrar_por(tickets: list[dict], **criterios) -> list[dict]:
    """Devuelve los tickets que cumplen TODOS los criterios que le pases.

        filtrar_por(tickets, prioridad="alta")
        filtrar_por(tickets, prioridad="alta", categoria="redes")

    Sin criterios, devolvé todos.

    Pista: `all(...)` te dice si se cumplen todas las condiciones de una
    colección. Una clave que el ticket no tiene cuenta como que no cumple.
    """
    return [
        tic
        for tic in tickets
        if all(
            clave in tic and tic[clave] == valor for clave, valor in criterios.items()
        )
    ]


# ===========================================================================
# El reporte. Ya está escrito: no lo toques, solo miralo salir.
# ===========================================================================
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    tickets = ejecutar_pipeline(TICKETS_CRUDOS)
    stats = resumen(tickets)

    print("=" * 58)
    print("SOPORTE — RESUMEN DE TICKETS".center(58))
    print("=" * 58)

    print("\n  PIPELINE")
    for orden in sorted(PASOS):
        etapa = PASOS[orden]
        descartados = etapa.entraron - etapa.salieron
        nota = f"  (-{descartados})" if descartados else ""
        print(
            f"    {orden}. {etapa.__name__:<24}"
            f"{etapa.entraron:>3} -> {etapa.salieron:<3}{nota}"
        )
    print(f"    cache de prioridades: {canonizar_prioridad.cache_info()}")

    print("\n  CIFRAS")
    print(f"    Tickets válidos  : {stats['tickets']}")
    print(f"    Descartados      : {len(TICKETS_CRUDOS) - stats['tickets']}")
    print(f"    Minutos totales  : {stats['minutos']}")
    print(f"    Promedio         : {stats['promedio']} min")
    print(f"    Usuarios         : {stats['usuarios']}")

    print("\n  CARGA POR USUARIO")
    for usuario, minutos in sorted(
        minutos_por_usuario(tickets).items(), key=lambda par: -par[1]
    ):
        print(f"    {usuario:<14} {'█' * (minutos // 15)} {minutos} min")

    print("\n  CATEGORÍAS")
    for puesto, (categoria, minutos) in enumerate(ranking_categorias(tickets), start=1):
        print(f"    {puesto}. {categoria:<12} {minutos} min")

    print("\n  PRIORIDAD ALTA")
    for ticket in filtrar_por(tickets, prioridad="alta"):
        print(
            f"    #{ticket['id']}  {ticket['usuario']:<14}"
            f"{ticket['categoria']:<12} {ticket['minutos']} min"
        )
    print("=" * 58)
