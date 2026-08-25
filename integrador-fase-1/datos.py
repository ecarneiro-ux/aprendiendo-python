"""
Datos de entrada del integrador.

Simulan lo que devolvería una API o una exportación de un sistema de ventas:
datos reales, o sea sucios. Espacios de más, mayúsculas inconsistentes, registros
incompletos y ventas en cero que nunca deberían haberse guardado.

NO edites este archivo. Tu trabajo es limpiarlo desde `analisis.py`.
"""

PEDIDOS_CRUDOS = [
    {
        "cliente": "  ana perez ",
        "email": "ANA@Mail.com",
        "producto": "teclado",
        "categoria": "accesorio",
        "total": 50,
    },
    {
        "cliente": "luis gomez",
        "email": "luis@mail.com",
        "producto": "monitor",
        "categoria": "pantalla",
        "total": 300,
    },
    {
        "cliente": "ANA PEREZ",
        "email": "ana@mail.com",
        "producto": "mouse",
        "categoria": "accesorio",
        "total": 20,
    },
    {
        # sin nombre de cliente -> registro inválido
        "cliente": "",
        "email": "fantasma@mail.com",
        "producto": "cable",
        "categoria": "accesorio",
        "total": 10,
    },
    {
        "cliente": "sofi ruiz",
        "email": "SOFI@MAIL.COM",
        "producto": "monitor",
        "categoria": "pantalla",
        "total": 300,
    },
    {
        "cliente": "luis gomez",
        "email": "luis@mail.com",
        "producto": "teclado",
        "categoria": "accesorio",
        "total": 50,
    },
    {
        # total en cero -> registro inválido
        "cliente": "beto diaz",
        "email": "beto@mail.com",
        "producto": "tablet",
        "categoria": "pantalla",
        "total": 0,
    },
    {
        # el nombre son solo espacios -> también inválido
        "cliente": "   ",
        "email": "otro@mail.com",
        "producto": "cable",
        "categoria": "accesorio",
        "total": 10,
    },
    {
        "cliente": "ana perez",
        "email": "ana@mail.com",
        "producto": "monitor",
        "categoria": "pantalla",
        "total": 300,
    },
    {
        "cliente": "beto diaz",
        "email": "beto@mail.com",
        "producto": "mouse",
        "categoria": "accesorio",
        "total": 20,
    },
]
