"""
Integrador Fase 1 — Solución de referencia.

LEÉ ESTO SOLO DESPUÉS de tener los 32 tests en verde y el reporte funcionando.

Tu versión también pasa. Esta muestra las decisiones que un pythonista tomaría,
que en un pipeline importan más que en ejercicios sueltos.
"""

from collections import Counter, defaultdict


def limpiar_pedido(pedido: dict) -> dict | None:
    cliente = pedido["cliente"].strip().title()
    # GUARD CLAUSE: el caso inválido se despacha primero y se sale.
    # Así el "camino feliz" queda al final, sin anidar, y los dos returns
    # explícitos le dicen al lector (y al type checker) qué sale por cada rama.
    if not cliente or pedido["total"] <= 0:
        return None
    return {**pedido, "cliente": cliente, "email": pedido["email"].strip().lower()}


def limpiar(crudos: list[dict]) -> list[dict]:
    # Dos pasos, no uno: guardamos el resultado y DESPUÉS filtramos.
    # Llamar a limpiar_pedido() dos veces por elemento no solo duplica el
    # trabajo: impide que el type checker estreche `dict | None` a `dict`.
    limpios = [limpiar_pedido(pedido) for pedido in crudos]
    # `is not None` y no truthiness: None acá es un centinela que significa
    # "inválido". Un dict vacío es falsy pero sería un resultado legítimo.
    return [pedido for pedido in limpios if pedido is not None]


def clientes_unicos(pedidos: list[dict]) -> set[str]:
    # Los pedidos que llegan acá YA están limpios: limpiar() corre una sola vez,
    # al principio del pipeline. Ninguna función río abajo vuelve a limpiar.
    return {pedido["email"] for pedido in pedidos}


def gasto_por_cliente(pedidos: list[dict]) -> dict[str, int]:
    # defaultdict(int) arranca cada clave nueva en 0.
    # `totales.get(email, 0) + total` sobre un dict común es igual de válido.
    gastos = defaultdict(int)
    for pedido in pedidos:
        gastos[pedido["email"]] += pedido["total"]
    return dict(gastos)


def ranking_clientes(pedidos: list[dict]) -> list[tuple[str, int]]:
    # El `-` invierte SOLO el gasto; el email queda ascendente.
    # reverse=True invertiría los dos criterios.
    return sorted(
        gasto_por_cliente(pedidos).items(), key=lambda item: (-item[1], item[0])
    )


def top_productos(pedidos: list[dict], n: int) -> list[tuple[str, int]]:
    # Counter acepta cualquier iterable: le pasamos una generator expression
    # en vez de construir la lista intermedia de productos.
    return Counter(pedido["producto"] for pedido in pedidos).most_common(n)


def productos_por_categoria(pedidos: list[dict]) -> dict[str, list[str]]:
    # Construir con la estructura que da la propiedad que necesitás (set =
    # unicidad), devolver la que pide el contrato (list ordenada).
    # Un set no tiene orden: sorted() resuelve la conversión y el orden juntos.
    por_categoria = defaultdict(set)
    for pedido in pedidos:
        por_categoria[pedido["categoria"]].add(pedido["producto"])
    return {cat: sorted(productos) for cat, productos in por_categoria.items()}


def clientes_recurrentes(pedidos: list[dict]) -> set[str]:
    # O(n): Counter recorre una sola vez. Con .count() sería O(n²).
    conteo = Counter(pedido["email"] for pedido in pedidos)
    return {email for email, veces in conteo.items() if veces > 1}


def resumen(pedidos: list[dict]) -> dict:
    # La guarda va PRIMERO, antes de cualquier cálculo. Si va al final, la
    # división por cero ocurre mucho antes de llegar a ella.
    # Regla: validá antes de calcular, no después.
    if not pedidos:
        return {
            "pedidos": 0,
            "facturado": 0,
            "ticket_promedio": 0.0,
            "clientes": 0,
            "cliente_top": None,
            "producto_top": None,
        }
    # De acá para abajo ya está garantizado que hay al menos un pedido:
    # ni la división ni los índices [0] pueden fallar.
    facturado = sum(pedido["total"] for pedido in pedidos)
    return {
        "pedidos": len(pedidos),
        "facturado": facturado,
        "ticket_promedio": round(facturado / len(pedidos), 2),
        "clientes": len(clientes_unicos(pedidos)),
        # Reusar las funciones de arriba en vez de recalcular: si mañana cambia
        # el criterio de desempate del ranking, se toca en un solo lugar.
        "cliente_top": ranking_clientes(pedidos)[0][0],
        "producto_top": top_productos(pedidos, 1)[0][0],
    }
