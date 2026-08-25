"""
Integrador de la Fase 1 — Analizador de ventas.

Te llegan pedidos crudos de una API. Tenés que limpiarlos y sacar un reporte.

A diferencia de los ejercicios sueltos, acá las funciones SE ENCADENAN: casi todas
reciben la salida de `limpiar()`. Si esa primera está mal, cae todo lo demás.

Cuando las tengas todas, corré:
    python integrador-fase-1/analisis.py
y vas a ver el reporte impreso.

Herramientas de la fase: comprehensions, sets, dicts, sorted(key=), lambda,
Counter, defaultdict, truthiness, unpacking.
"""

import sys
from collections import Counter, defaultdict

from datos import PEDIDOS_CRUDOS


# ---------------------------------------------------------------------------
# 1a. LIMPIAR UN SOLO PEDIDO
#
# Antes de arrancar, corré:  python integrador-fase-1/demo_copiar_dict.py
# Explica cómo copiar un dict cambiándole claves, que es la pieza que falta acá.
# ---------------------------------------------------------------------------
def limpiar_pedido(pedido: dict) -> dict | None:
    """Limpia UN pedido. Devuelve el dict limpio, o None si el pedido es inválido.

    Es una función común y corriente: un par de ifs y un return.
    NO hace falta ninguna comprehension acá.

    Pasos:
      1. Calculá el cliente limpio: sin espacios en los extremos y con
         iniciales en mayúscula.   "  ana perez "  ->  "Ana Perez"
      2. Si ese cliente quedó vacío, o si el total no es mayor a 0,
         devolvé None (el pedido es inválido).
      3. Si no, devolvé un dict NUEVO igual al original pero con el cliente
         limpio y el email sin espacios y en minúscula.
         Las claves "producto", "categoria" y "total" se copian tal cual.
         El dict que te pasaron NO se puede modificar.

    >>> limpiar_pedido({"cliente": " ana ", "email": "A@X.com", "total": 5})
    {'cliente': 'Ana', 'email': 'a@x.com', 'total': 5}
    >>> limpiar_pedido({"cliente": "  ", "email": "a@x.com", "total": 5}) is None
    True
    """
    cliente = pedido["cliente"].strip()
    email = pedido["email"].strip().lower()
    total = pedido["total"]
    if not cliente or total <= 0:
        return None
    return {**pedido, "cliente": cliente.title(), "email": email}

    # {**pedido, "cliente": "Ana Perez"}
    """
    if not cliente or total <= 0:
        return None
    return {**pedido, "cliente": cliente.title(), "email": email}
    """


# ---------------------------------------------------------------------------
# 1b. APLICARLO A TODOS
# ---------------------------------------------------------------------------
def limpiar(crudos: list[dict]) -> list[dict]:
    """Limpia todos los pedidos y descarta los inválidos.

    Con `limpiar_pedido` funcionando, esto son dos líneas: aplicalo a cada
    pedido, y quedate solo con los que no dieron None.

    Ojo: no lo llames dos veces por pedido (una para calcular y otra para
    preguntar si es None). Guardá los resultados en una lista y después filtrá.
    """
    limpios = [limpiar_pedido(cru) for cru in crudos]
    return [pedido for pedido in limpios if pedido is not None]


# ---------------------------------------------------------------------------
# 2. Clientes distintos
# ---------------------------------------------------------------------------
def clientes_unicos(pedidos: list[dict]) -> set[str]:
    """Devuelve el conjunto de emails distintos.

    El email es el identificador del cliente: dos pedidos con el mismo email
    son de la misma persona, aunque el nombre venga escrito distinto.
    """
    return {repetidos["email"] for repetidos in pedidos}


# ---------------------------------------------------------------------------
# 3. Cuánto gastó cada uno
# ---------------------------------------------------------------------------
def gasto_por_cliente(pedidos: list[dict]) -> dict[str, int]:
    """Suma el total gastado por cada email.

    >>> gasto_por_cliente([{"email": "a@x.com", "total": 10},
    ...                    {"email": "a@x.com", "total": 5}])
    {'a@x.com': 15}
    """
    totales = {}
    for pedid in pedidos:
        cliente = pedid["email"]
        totales[cliente] = totales.get(cliente, 0) + pedid["total"]
    return totales


# ---------------------------------------------------------------------------
# 4. Ranking de clientes
# ---------------------------------------------------------------------------
def ranking_clientes(pedidos: list[dict]) -> list[tuple[str, int]]:
    """Devuelve pares (email, gasto) del que más gastó al que menos.

    Si dos empatan en gasto, van en orden alfabético de email ASCENDENTE.
    Reusá `gasto_por_cliente`: no repitas la suma acá.
    """
    return sorted(gasto_por_cliente(pedidos).items(), key=lambda ped: (-ped[1], ped[0]))


# ---------------------------------------------------------------------------
# 5. Productos más vendidos
# ---------------------------------------------------------------------------
def top_productos(pedidos: list[dict], n: int) -> list[tuple[str, int]]:
    """Devuelve los n productos más vendidos con su cantidad de pedidos,
    de mayor a menor.
    """
    ventas = Counter(p["producto"] for p in pedidos)
    return ventas.most_common(n)


# ---------------------------------------------------------------------------
# 6. Agrupar por categoría
# ---------------------------------------------------------------------------
def productos_por_categoria(pedidos: list[dict]) -> dict[str, list[str]]:
    """Devuelve, por cada categoría, la lista de productos DISTINTOS que se
    vendieron, ordenados alfabéticamente.

    Devolvé un dict común, no un defaultdict.

    >>> productos_por_categoria([{"categoria": "a", "producto": "z"},
    ...                          {"categoria": "a", "producto": "z"},
    ...                          {"categoria": "a", "producto": "b"}])
    {'a': ['b', 'z']}
    """
    por_cat = defaultdict(set)
    # aca me tuve que ayudar de internet porque no entendia como sacar los duplicados
    for cat in pedidos:
        por_cat[cat["categoria"]].add(cat["producto"])
    return {categoria: sorted(productos) for categoria, productos in por_cat.items()}


# ---------------------------------------------------------------------------
# 7. Clientes que volvieron
# ---------------------------------------------------------------------------
def clientes_recurrentes(pedidos: list[dict]):  # -> set[str]
    """Devuelve los emails de los clientes con MÁS DE UN pedido.

    Tiene que recorrer los pedidos una sola vez: nada de `.count()`.
    """

    emails_re = Counter(p["email"] for p in pedidos)
    return {clientes for clientes, veces in emails_re.items() if veces > 1}


# ---------------------------------------------------------------------------
# 8. EL RESUMEN — acá se junta todo
# ---------------------------------------------------------------------------
def resumen(pedidos: list[dict]):  # -> dict
    """Arma el resumen final reusando las funciones de arriba.

    Devolvé un dict con exactamente estas claves:

      "pedidos"          -> cantidad de pedidos válidos (int)
      "facturado"        -> suma de todos los totales (int)
      "ticket_promedio"  -> facturado / pedidos, redondeado a 2 decimales (float)
      "clientes"         -> cantidad de clientes distintos (int)
      "cliente_top"      -> email del que más gastó (str)
      "producto_top"     -> producto más vendido (str)

    Con una lista vacía, devolvé:
      {"pedidos": 0, "facturado": 0, "ticket_promedio": 0.0,
       "clientes": 0, "cliente_top": None, "producto_top": None}

    Pista: `round(x, 2)` redondea a 2 decimales.
    """

    if not pedidos:
        return {
            "pedidos": 0,
            "facturado": 0,
            "ticket_promedio": 0.0,
            "clientes": 0,
            "cliente_top": None,
            "producto_top": None,
        }
    # todos_pedidos = Counter(p["email"] for p in pedidos)
    pedidos_v: int = len(pedidos)

    todos_gastos = gasto_por_cliente(pedidos)
    facturado: int = sum(todos_gastos.values())

    ticket_promedio: float = facturado / pedidos_v
    clientes_d: int = len(clientes_unicos(pedidos))
    cliente_top: str | None = ranking_clientes(pedidos)[0][0]  # antes del ruff check: [e for e, _ in ranking_clientes(pedidos)][0]
    producto_top: str | None = top_productos(pedidos,1)[0][0]  # antes del ruff check: [p for p, _ in top_productos(pedidos, 1)][0]
    return {
        "pedidos": pedidos_v,
        "facturado": facturado,
        "ticket_promedio": round(ticket_promedio, 2),
        "clientes": clientes_d,
        "cliente_top": cliente_top,
        "producto_top": producto_top,
    }


# ---------------------------------------------------------------------------
# El reporte — ya está escrito, no lo toques.
# Corré `python integrador-fase-1/analisis.py` cuando termines.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # En Windows la consola puede caer a cp1252 (por ejemplo al redirigir la
    # salida a un archivo), y ahí los caracteres ★ y █ revientan. Esto fuerza
    # UTF-8 en la salida pase lo que pase.
    sys.stdout.reconfigure(encoding="utf-8")

    # print(gasto_por_cliente([{"email": "a@x.com", "total": 10},{"email": "a@x.com", "total": 5}]))
    pedidos = limpiar(PEDIDOS_CRUDOS)
    # print(resumen(pedidos))
    stats = resumen(pedidos)

    print("=" * 52)
    print("REPORTE DE VENTAS".center(52))
    print("=" * 52)
    print(f"  Pedidos válidos : {stats['pedidos']}")
    print(f"  Descartados     : {len(PEDIDOS_CRUDOS) - stats['pedidos']}")
    print(f"  Facturado       : ${stats['facturado']}")
    print(f"  Ticket promedio : ${stats['ticket_promedio']}")
    print(f"  Clientes        : {stats['clientes']}")

    print("\n  RANKING DE CLIENTES")
    for puesto, (email, gasto) in enumerate(ranking_clientes(pedidos), start=1):
        marca = " ★" if email in clientes_recurrentes(pedidos) else ""
        print(f"    {puesto}. {email:<20} ${gasto}{marca}")
    print("    (★ = compró más de una vez)")

    print("\n  TOP PRODUCTOS")
    for producto, veces in top_productos(pedidos, 3):
        print(f"    {producto:<12} {'█' * veces} {veces}")

    print("\n  CATÁLOGO POR CATEGORÍA")
    for categoria, productos in sorted(productos_por_categoria(pedidos).items()):
        print(f"    {categoria:<12} {', '.join(productos)}")
    print("=" * 52)
