"""
Integrador de la Fase 2 — Solución de referencia.

LEÉ ESTO SOLO DESPUÉS de tener tus 36 tests en verde.
"""

import sys
from collections import Counter
from collections.abc import Callable
from functools import cache, wraps

from datos_soporte import TICKETS_CRUDOS

PASOS: dict[int, Callable] = {}


def contar_registros(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        # `args[0]` en vez de `len(*args)`: decir "el primer argumento" es más
        # claro que desempaquetar todo y confiar en que venga uno solo.
        #
        # Y `=`, no `+=`: el atributo se llama "entraron", no "entraron en
        # total desde que arrancó el proceso". Con `+=`, correr el pipeline
        # dos veces te duplica los números del reporte.
        envoltorio.entraron = len(args[0])  # type: ignore[attr-defined]
        resultado = func(*args, **kwargs)
        envoltorio.salieron = len(resultado)  # type: ignore[attr-defined]
        return resultado

    envoltorio.entraron = 0  # type: ignore[attr-defined]
    envoltorio.salieron = 0  # type: ignore[attr-defined]
    return envoltorio


def paso(orden: int):
    def decorador(func):
        PASOS[orden] = func
        return func

    return decorador


def ejecutar_pipeline(tickets: list[dict]) -> list[dict]:
    resultado = tickets
    for orden in sorted(PASOS):
        resultado = PASOS[orden](resultado)
    return resultado


def exige_datos(func):
    @wraps(func)
    def envoltorio(*args, **kwargs):
        # `if not args[0]`, no `== []`. Truthiness cubre lista, tupla, dict,
        # set y string vacíos de una; `== []` solo detecta la lista.
        if not args[0]:
            raise ValueError("no hay datos para procesar")
        return func(*args, **kwargs)

    return envoltorio


# Cada paso hace UNA cosa y se llama como esa cosa. Si `descartar_incompletos`
# también normalizara texto, su nombre mentiría y el paso 2 no tendría trabajo.
@paso(1)
@contar_registros
def descartar_incompletos(tickets: list[dict]) -> list[dict]:
    return [t for t in tickets if t["usuario"].strip() and t["minutos"] > 0]


@paso(2)
@contar_registros
def normalizar_texto(tickets: list[dict]) -> list[dict]:
    # No llama a `descartar_incompletos`: cuando este paso corre, el motor ya
    # lo ejecutó. Volver a llamarlo es trabajo repetido y además ensucia las
    # métricas (el paso 1 aparecería procesando tickets que ya había limpiado).
    return [
        {
            **t,
            "usuario": t["usuario"].strip().title(),
            "categoria": t["categoria"].strip().lower(),
        }
        for t in tickets
    ]


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
    # `.get(clave, default)` hace en una búsqueda lo que el `if not in` + el
    # indexado hacen en dos.
    return PRIORIDADES.get(texto.strip().lower(), "media")


@paso(3)
@contar_registros
def unificar_prioridad(tickets: list[dict]) -> list[dict]:
    return [{**t, "prioridad": canonizar_prioridad(t["prioridad"])} for t in tickets]


@exige_datos
def resumen(tickets: list[dict]) -> dict:
    minutos = sum(t["minutos"] for t in tickets)
    return {
        "tickets": len(tickets),
        "minutos": minutos,
        "promedio": round(minutos / len(tickets), 2),
        # Para "cuántos distintos hay", un set. Un Counter cuenta cuántas veces
        # aparece cada uno — trabajo que después se tira.
        "usuarios": len({t["usuario"] for t in tickets}),
    }


def minutos_por_usuario(tickets: list[dict]) -> dict[str, int]:
    # Nombre en minúsculas: MAYÚSCULAS es la convención para constantes de
    # módulo. Y no es una lista, es un acumulador.
    acumulado = Counter()
    for ticket in tickets:
        acumulado[ticket["usuario"]] += ticket["minutos"]
    return dict(acumulado)


def ranking_categorias(tickets: list[dict]) -> list[tuple[str, int]]:
    acumulado = Counter()
    for ticket in tickets:
        acumulado[ticket["categoria"]] += ticket["minutos"]
    # `-minutos` invierte solo ese criterio; el alfabético queda ascendente.
    return sorted(acumulado.items(), key=lambda par: (-par[1], par[0]))


def filtrar_por(tickets: list[dict], **criterios) -> list[dict]:
    return [
        t
        # Desempaquetar en el for se lee; `c[0]` y `c[1]` hay que descifrarlos.
        for t in tickets
        if all(t.get(clave) == valor for clave, valor in criterios.items())
    ]


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
