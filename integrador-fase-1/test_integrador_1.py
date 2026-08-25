"""Tests del integrador de la Fase 1. NO los edites."""

import copy
import inspect

from analisis import (
    clientes_recurrentes,
    clientes_unicos,
    gasto_por_cliente,
    limpiar,
    limpiar_pedido,
    productos_por_categoria,
    ranking_clientes,
    resumen,
    top_productos,
)
from datos import PEDIDOS_CRUDOS


def pedido(email, total=10, producto="x", categoria="c", cliente="Ana"):
    """Fabrica un pedido ya limpio, para tests chicos y legibles."""
    return {
        "cliente": cliente,
        "email": email,
        "producto": producto,
        "categoria": categoria,
        "total": total,
    }


LIMPIOS = limpiar(PEDIDOS_CRUDOS) if limpiar(PEDIDOS_CRUDOS) is not None else []


# 1a. limpiar_pedido --------------------------------------------------------
# Empezá por estos cuatro. Son los más chicos de todo el integrador.
def test_limpiar_pedido_normaliza_el_cliente():
    resultado = limpiar_pedido({**pedido("a@x.com"), "cliente": "  ana perez "})
    assert resultado["cliente"] == "Ana Perez"


def test_limpiar_pedido_normaliza_el_email():
    assert limpiar_pedido(pedido("  ANA@Mail.com  "))["email"] == "ana@mail.com"


def test_limpiar_pedido_conserva_las_demas_claves():
    resultado = limpiar_pedido(pedido("a@x.com", 25, "mouse", "accesorio"))
    assert resultado["producto"] == "mouse"
    assert resultado["categoria"] == "accesorio"
    assert resultado["total"] == 25


def test_limpiar_pedido_devuelve_none_si_es_invalido():
    assert limpiar_pedido({**pedido("a@x.com"), "cliente": ""}) is None
    assert limpiar_pedido({**pedido("a@x.com"), "cliente": "   "}) is None
    assert limpiar_pedido(pedido("a@x.com", total=0)) is None
    assert limpiar_pedido(pedido("a@x.com", total=-5)) is None


def test_limpiar_pedido_no_modifica_la_entrada():
    original = {**pedido("A@X.com"), "cliente": "  ana  "}
    copia = dict(original)
    limpiar_pedido(original)
    assert original == copia, "modificaste el dict que te pasaron"


# 1b. limpiar ---------------------------------------------------------------
def test_limpiar_descarta_los_invalidos():
    assert len(limpiar(PEDIDOS_CRUDOS)) == 7


def test_limpiar_normaliza_el_nombre():
    resultado = limpiar([{**pedido("a@x.com"), "cliente": "  ana perez "}])
    assert resultado[0]["cliente"] == "Ana Perez"


def test_limpiar_normaliza_el_email():
    resultado = limpiar([{**pedido("  ANA@Mail.com  ")}])
    assert resultado[0]["email"] == "ana@mail.com"


def test_limpiar_descarta_cliente_vacio_o_con_espacios():
    assert limpiar([{**pedido("a@x.com"), "cliente": ""}]) == []
    assert limpiar([{**pedido("a@x.com"), "cliente": "   "}]) == []


def test_limpiar_descarta_total_cero_o_negativo():
    assert limpiar([pedido("a@x.com", total=0)]) == []
    assert limpiar([pedido("a@x.com", total=-5)]) == []


def test_limpiar_conserva_las_demas_claves():
    resultado = limpiar([pedido("a@x.com", producto="mouse", categoria="accesorio")])
    assert resultado[0]["producto"] == "mouse"
    assert resultado[0]["categoria"] == "accesorio"
    assert resultado[0]["total"] == 10


def test_limpiar_no_modifica_la_entrada():
    """El pipeline no puede ensuciar los datos de origen."""
    copia = copy.deepcopy(PEDIDOS_CRUDOS)
    limpiar(PEDIDOS_CRUDOS)
    assert PEDIDOS_CRUDOS == copia, "modificaste los dicts originales"


# 2. clientes_unicos --------------------------------------------------------
def test_clientes_unicos():
    assert clientes_unicos(LIMPIOS) == {
        "ana@mail.com",
        "luis@mail.com",
        "sofi@mail.com",
        "beto@mail.com",
    }
    assert clientes_unicos([]) == set()


# 3. gasto_por_cliente ------------------------------------------------------
def test_gasto_por_cliente_suma():
    pedidos = [pedido("a@x.com", 10), pedido("a@x.com", 5), pedido("b@x.com", 7)]
    assert gasto_por_cliente(pedidos) == {"a@x.com": 15, "b@x.com": 7}


def test_gasto_por_cliente_dataset():
    assert gasto_por_cliente(LIMPIOS) == {
        "ana@mail.com": 370,
        "luis@mail.com": 350,
        "sofi@mail.com": 300,
        "beto@mail.com": 20,
    }


def test_gasto_por_cliente_vacio():
    assert gasto_por_cliente([]) == {}


# 4. ranking_clientes -------------------------------------------------------
def test_ranking_clientes():
    assert ranking_clientes(LIMPIOS) == [
        ("ana@mail.com", 370),
        ("luis@mail.com", 350),
        ("sofi@mail.com", 300),
        ("beto@mail.com", 20),
    ]


def test_ranking_desempata_alfabeticamente_ascendente():
    """Empatados en gasto: alfabético normal, NO invertido."""
    pedidos = [pedido("zoe@x.com", 5), pedido("ana@x.com", 5), pedido("luis@x.com", 9)]
    assert ranking_clientes(pedidos) == [
        ("luis@x.com", 9),
        ("ana@x.com", 5),
        ("zoe@x.com", 5),
    ]


def test_ranking_vacio():
    assert ranking_clientes([]) == []


# 5. top_productos ----------------------------------------------------------
def test_top_productos():
    assert top_productos(LIMPIOS, 1) == [("monitor", 3)]
    assert dict(top_productos(LIMPIOS, 3)) == {"monitor": 3, "teclado": 2, "mouse": 2}


def test_top_productos_n_mayor_al_total():
    assert top_productos([pedido("a@x.com", producto="uno")], 10) == [("uno", 1)]


def test_top_productos_vacio():
    assert top_productos([], 3) == []


# 6. productos_por_categoria ------------------------------------------------
def test_productos_por_categoria():
    assert productos_por_categoria(LIMPIOS) == {
        "accesorio": ["mouse", "teclado"],
        "pantalla": ["monitor"],
    }


def test_productos_por_categoria_sin_duplicados_y_ordenado():
    pedidos = [
        pedido("a@x.com", producto="z", categoria="a"),
        pedido("a@x.com", producto="z", categoria="a"),
        pedido("a@x.com", producto="b", categoria="a"),
    ]
    assert productos_por_categoria(pedidos) == {"a": ["b", "z"]}


def test_productos_por_categoria_devuelve_dict_comun():
    resultado = productos_por_categoria(LIMPIOS)
    assert type(resultado) is dict, "convertilo con dict(...)"
    assert productos_por_categoria([]) == {}


# 7. clientes_recurrentes ---------------------------------------------------
def test_clientes_recurrentes():
    assert clientes_recurrentes(LIMPIOS) == {"ana@mail.com", "luis@mail.com"}


def test_clientes_recurrentes_ninguno():
    assert clientes_recurrentes([pedido("a@x.com"), pedido("b@x.com")]) == set()
    assert clientes_recurrentes([]) == set()


def test_clientes_recurrentes_sin_count():
    cuerpo = inspect.getsource(clientes_recurrentes).split('"""')[-1]
    codigo = "\n".join(linea.split("#")[0] for linea in cuerpo.splitlines())
    assert ".count(" not in codigo, "usá Counter, no .count()"


# 8. resumen ----------------------------------------------------------------
def test_resumen():
    assert resumen(LIMPIOS) == {
        "pedidos": 7,
        "facturado": 1040,
        "ticket_promedio": 148.57,
        "clientes": 4,
        "cliente_top": "ana@mail.com",
        "producto_top": "monitor",
    }


def test_resumen_vacio():
    """Sin pedidos no se puede dividir por cero ni sacar un máximo."""
    assert resumen([]) == {
        "pedidos": 0,
        "facturado": 0,
        "ticket_promedio": 0.0,
        "clientes": 0,
        "cliente_top": None,
        "producto_top": None,
    }


def test_resumen_ticket_redondeado():
    pedidos = [pedido("a@x.com", 10), pedido("b@x.com", 10), pedido("c@x.com", 11)]
    assert resumen(pedidos)["ticket_promedio"] == 10.33


def test_resumen_reusa_las_otras_funciones():
    """No copies y pegues la lógica: llamá a las funciones que ya escribiste."""
    codigo = inspect.getsource(resumen)
    usadas = [
        n
        for n in ("gasto_por_cliente", "clientes_unicos", "top_productos", "ranking")
        if n in codigo
    ]
    assert usadas, "resumen() tiene que apoyarse en las funciones anteriores"
