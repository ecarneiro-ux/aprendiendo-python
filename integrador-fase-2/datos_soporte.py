"""
Datos de entrada del integrador de la Fase 2.

Simulan la exportación de un sistema de tickets de soporte: espacios de más,
mayúsculas inconsistentes, prioridades escritas de siete formas distintas,
tickets sin usuario y tickets con minutos en cero o negativos.

NO edites este archivo. Tu trabajo es procesarlo desde `pipeline.py`.

(Se llama `datos_soporte.py` y no `datos.py` porque el integrador de la Fase 1
ya tiene un `datos.py`, y Python no puede tener dos módulos con el mismo nombre
cargados a la vez: el segundo test recibiría el módulo del primero.)
"""

TICKETS_CRUDOS = [
    {
        "id": 101,
        "usuario": "  ana perez ",
        "categoria": " Redes ",
        "prioridad": "ALTA",
        "minutos": 45,
    },
    {
        "id": 102,
        "usuario": "LUIS GOMEZ",
        "categoria": "hardware",
        "prioridad": "media",
        "minutos": 30,
    },
    {
        "id": 103,
        "usuario": "ana perez",
        "categoria": "SOFTWARE ",
        "prioridad": "a",
        "minutos": 120,
    },
    {
        # sin usuario -> ticket inválido
        "id": 104,
        "usuario": "",
        "categoria": "redes",
        "prioridad": "alta",
        "minutos": 20,
    },
    {
        "id": 105,
        "usuario": "sofi ruiz",
        "categoria": " Accesos",
        "prioridad": " baja ",
        "minutos": 15,
    },
    {
        # prioridad que no existe en la tabla -> cae a "media"
        "id": 106,
        "usuario": "  luis gomez",
        "categoria": "redes ",
        "prioridad": "urgentísimo",
        "minutos": 60,
    },
    {
        "id": 107,
        "usuario": "beto diaz",
        "categoria": "Hardware",
        "prioridad": "baja",
        "minutos": 90,
    },
    {
        "id": 108,
        "usuario": "ana perez ",
        "categoria": "accesos",
        "prioridad": "media",
        "minutos": 25,
    },
    {
        # usuario en blanco (no vacío: espacios) -> ticket inválido
        "id": 109,
        "usuario": "   ",
        "categoria": "software",
        "prioridad": "alta",
        "minutos": 40,
    },
    {
        "id": 110,
        "usuario": "sofi ruiz",
        "categoria": "REDES",
        "prioridad": "high",
        "minutos": 75,
    },
    {
        # prioridad vacía -> cae a "media"
        "id": 111,
        "usuario": "luis gomez",
        "categoria": "software",
        "prioridad": "",
        "minutos": 50,
    },
    {
        # minutos en cero -> ticket inválido
        "id": 112,
        "usuario": "beto diaz ",
        "categoria": " software ",
        "prioridad": "low",
        "minutos": 0,
    },
    {
        "id": 113,
        "usuario": "ana perez",
        "categoria": "hardware",
        "prioridad": "ALTA",
        "minutos": 35,
    },
    {
        # minutos negativos -> ticket inválido
        "id": 114,
        "usuario": "sofi ruiz ",
        "categoria": "redes",
        "prioridad": "m",
        "minutos": -10,
    },
    {
        "id": 115,
        "usuario": "beto diaz",
        "categoria": "accesos",
        "prioridad": "baja",
        "minutos": 55,
    },
]
