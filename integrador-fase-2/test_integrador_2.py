"""Tests del integrador de la Fase 2. NO los edites."""

import pytest
from datos_soporte import TICKETS_CRUDOS
from pipeline import (
    PASOS,
    canonizar_prioridad,
    contar_registros,
    descartar_incompletos,
    ejecutar_pipeline,
    exige_datos,
    filtrar_por,
    minutos_por_usuario,
    normalizar_texto,
    paso,
    ranking_categorias,
    resumen,
    unificar_prioridad,
)


def ticket(usuario="Ana Perez", categoria="redes", prioridad="alta", minutos=10, id_=1):
    """Fabrica un ticket ya limpio, para tests chicos y legibles."""
    return {
        "id": id_,
        "usuario": usuario,
        "categoria": categoria,
        "prioridad": prioridad,
        "minutos": minutos,
    }


# 1. contar_registros --------------------------------------------------------
def test_contar_registros_devuelve_lo_mismo():
    @contar_registros
    def sin_ceros(numeros):
        return [n for n in numeros if n]

    assert sin_ceros([0, 1, 2, 0]) == [1, 2]


def test_contar_registros_arranca_en_cero():
    @contar_registros
    def identidad(items):
        return items

    assert (identidad.entraron, identidad.salieron) == (0, 0)


def test_contar_registros_cuenta_entradas_y_salidas():
    @contar_registros
    def sin_ceros(numeros):
        return [n for n in numeros if n]

    sin_ceros([0, 1, 2, 0])
    assert (sin_ceros.entraron, sin_ceros.salieron) == (4, 2)


def test_contar_registros_conserva_el_nombre():
    @contar_registros
    def identidad(items):
        return items

    assert identidad.__name__ == "identidad", "te falta @wraps(func)"


# 2. paso --------------------------------------------------------------------
def test_paso_registra_la_funcion():
    try:

        @paso(99)
        def falso(tickets):
            return tickets

        assert PASOS[99] is falso
    finally:
        PASOS.pop(99, None)


def test_paso_no_envuelve():
    try:

        @paso(98)
        def falso(tickets):
            return tickets

        assert falso.__name__ == "falso"
        assert falso([1, 2]) == [1, 2]
    finally:
        PASOS.pop(98, None)


def test_los_tres_pasos_estan_declarados():
    """Si esto falla, revisá el ORDEN en que apilaste @paso y @contar_registros."""
    orden_mal = (
        "en PASOS quedó la función sin instrumentar: "
        "@paso(N) va ARRIBA de @contar_registros"
    )
    assert sorted(PASOS) == [1, 2, 3]
    assert hasattr(PASOS[1], "entraron"), orden_mal
    assert PASOS[1] is descartar_incompletos, orden_mal
    assert PASOS[2] is normalizar_texto, orden_mal
    assert PASOS[3] is unificar_prioridad, orden_mal


# 3. ejecutar_pipeline -------------------------------------------------------
def test_ejecutar_pipeline_encadena_en_orden():
    esperado = unificar_prioridad(
        normalizar_texto(descartar_incompletos(TICKETS_CRUDOS))
    )
    assert ejecutar_pipeline(TICKETS_CRUDOS) == esperado


def test_ejecutar_pipeline_sobre_los_datos_reales():
    tickets = ejecutar_pipeline(TICKETS_CRUDOS)
    assert len(tickets) == 11
    assert all(t["prioridad"] in {"alta", "media", "baja"} for t in tickets)
    assert all(t["categoria"] == t["categoria"].strip().lower() for t in tickets)


# 4. exige_datos -------------------------------------------------------------
def test_exige_datos_deja_pasar():
    @exige_datos
    def contar(items):
        return len(items)

    assert contar([1, 2]) == 2


def test_exige_datos_rechaza_lo_vacio():
    @exige_datos
    def contar(items):
        return len(items)

    with pytest.raises(ValueError):
        contar([])


def test_exige_datos_no_llega_a_llamar():
    ejecuciones = []

    @exige_datos
    def contar(items):
        ejecuciones.append(items)
        return len(items)

    with pytest.raises(ValueError):
        contar([])
    assert ejecuciones == [], "validaste después de llamar a func"


# 5. descartar_incompletos ---------------------------------------------------
def test_descartar_incompletos_saca_los_sin_usuario():
    tickets = [ticket(usuario="Ana"), ticket(usuario=""), ticket(usuario="   ")]
    assert descartar_incompletos(tickets) == [ticket(usuario="Ana")]


def test_descartar_incompletos_saca_los_minutos_no_positivos():
    tickets = [ticket(minutos=5), ticket(minutos=0), ticket(minutos=-3)]
    assert descartar_incompletos(tickets) == [ticket(minutos=5)]


def test_descartar_incompletos_no_toca_la_lista_original():
    tickets = [ticket(usuario="Ana"), ticket(usuario="")]
    descartar_incompletos(tickets)
    assert len(tickets) == 2, "usaste .remove()/.pop() sobre la lista que te pasaron"


# 6. normalizar_texto --------------------------------------------------------
def test_normalizar_texto_arregla_el_usuario():
    assert (
        normalizar_texto([ticket(usuario="  ana perez ")])[0]["usuario"] == "Ana Perez"
    )


def test_normalizar_texto_arregla_la_categoria():
    assert normalizar_texto([ticket(categoria=" Redes ")])[0]["categoria"] == "redes"


def test_normalizar_texto_no_muta_los_originales():
    original = ticket(usuario="  ana perez ", categoria=" Redes ")
    normalizar_texto([original])
    assert original["usuario"] == "  ana perez "
    assert original["categoria"] == " Redes "


# 7. canonizar_prioridad -----------------------------------------------------
def test_canonizar_prioridad_variantes():
    assert canonizar_prioridad("ALTA") == "alta"
    assert canonizar_prioridad("  a ") == "alta"
    assert canonizar_prioridad("High") == "alta"
    assert canonizar_prioridad("LOW") == "baja"


def test_canonizar_prioridad_desconocida_es_media():
    assert canonizar_prioridad("urgentísimo") == "media"
    assert canonizar_prioridad("") == "media"
    assert canonizar_prioridad("   ") == "media"


def test_canonizar_prioridad_esta_cacheada():
    assert hasattr(canonizar_prioridad, "cache_info"), (
        "le falta el decorador de functools"
    )


# 8. unificar_prioridad ------------------------------------------------------
def test_unificar_prioridad_canoniza():
    tickets = [ticket(prioridad="ALTA"), ticket(prioridad="b"), ticket(prioridad="?")]
    assert [t["prioridad"] for t in unificar_prioridad(tickets)] == [
        "alta",
        "baja",
        "media",
    ]


def test_unificar_prioridad_no_muta_los_originales():
    original = ticket(prioridad="ALTA")
    unificar_prioridad([original])
    assert original["prioridad"] == "ALTA"


# 9. resumen -----------------------------------------------------------------
def test_resumen():
    tickets = [
        ticket(usuario="Ana", minutos=30),
        ticket(usuario="Luis", minutos=60),
        ticket(usuario="Ana", minutos=30),
    ]
    assert resumen(tickets) == {
        "tickets": 3,
        "minutos": 120,
        "promedio": 40.0,
        "usuarios": 2,
    }


def test_resumen_redondea_a_dos_decimales():
    tickets = [ticket(minutos=10), ticket(minutos=10), ticket(minutos=11)]
    assert resumen(tickets)["promedio"] == 10.33


def test_resumen_sin_tickets_lanza_valueerror():
    """La guarda va antes de dividir. Si no, es ZeroDivisionError."""
    with pytest.raises(ValueError):
        resumen([])


# 10. minutos_por_usuario ----------------------------------------------------
def test_minutos_por_usuario():
    tickets = [
        ticket(usuario="Ana", minutos=30),
        ticket(usuario="Luis", minutos=60),
        ticket(usuario="Ana", minutos=15),
    ]
    assert minutos_por_usuario(tickets) == {"Ana": 45, "Luis": 60}


def test_minutos_por_usuario_devuelve_un_dict_comun():
    resultado = minutos_por_usuario([ticket(usuario="Ana", minutos=5)])
    assert type(resultado) is dict, "convertilo con dict(...) antes de devolverlo"


def test_minutos_por_usuario_sin_tickets():
    assert minutos_por_usuario([]) == {}


# 11. ranking_categorias -----------------------------------------------------
def test_ranking_categorias():
    tickets = [
        ticket(categoria="redes", minutos=30),
        ticket(categoria="software", minutos=100),
        ticket(categoria="redes", minutos=20),
    ]
    assert ranking_categorias(tickets) == [("software", 100), ("redes", 50)]


def test_ranking_categorias_empate_va_alfabetico():
    tickets = [
        ticket(categoria="software", minutos=50),
        ticket(categoria="accesos", minutos=50),
        ticket(categoria="hardware", minutos=50),
    ]
    assert ranking_categorias(tickets) == [
        ("accesos", 50),
        ("hardware", 50),
        ("software", 50),
    ]


def test_ranking_categorias_sin_tickets():
    assert ranking_categorias([]) == []


# 12. filtrar_por ------------------------------------------------------------
def test_filtrar_por_un_criterio():
    tickets = [ticket(prioridad="alta", id_=1), ticket(prioridad="baja", id_=2)]
    assert [t["id"] for t in filtrar_por(tickets, prioridad="alta")] == [1]


def test_filtrar_por_dos_criterios_es_un_and():
    tickets = [
        ticket(prioridad="alta", categoria="redes", id_=1),
        ticket(prioridad="alta", categoria="software", id_=2),
        ticket(prioridad="baja", categoria="redes", id_=3),
    ]
    encontrados = filtrar_por(tickets, prioridad="alta", categoria="redes")
    assert [t["id"] for t in encontrados] == [1]


def test_filtrar_por_sin_criterios_devuelve_todo():
    tickets = [ticket(id_=1), ticket(id_=2)]
    assert filtrar_por(tickets) == tickets


# Integración ----------------------------------------------------------------
def test_el_reporte_completo_da_los_numeros_esperados():
    tickets = ejecutar_pipeline(TICKETS_CRUDOS)
    assert resumen(tickets) == {
        "tickets": 11,
        "minutos": 600,
        "promedio": 54.55,
        "usuarios": 4,
    }
    assert minutos_por_usuario(tickets) == {
        "Ana Perez": 225,
        "Luis Gomez": 140,
        "Sofi Ruiz": 90,
        "Beto Diaz": 145,
    }
    assert ranking_categorias(tickets) == [
        ("redes", 180),
        ("software", 170),
        ("hardware", 155),
        ("accesos", 95),
    ]
    assert len(filtrar_por(tickets, prioridad="alta")) == 4
