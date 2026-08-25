"""
La pieza que falta: copiar un dict cambiándole algunas claves.

Corré esto:  python integrador-fase-1/demo_copiar_dict.py
"""

pedido = {"cliente": "  ana perez ", "email": "ANA@Mail.com", "total": 50}

print("=" * 60)
print("EL PROBLEMA")
print("=" * 60)

# Lo intuitivo viniendo de C# sería modificar el objeto:
copia_mala = pedido
copia_mala["cliente"] = "Ana Perez"
print("  pedido original ->", pedido["cliente"])
print("  ...se modificó, porque `copia_mala = pedido` NO copia nada:")
print("  son el mismo objeto:", copia_mala is pedido)

# Lo dejamos como estaba para seguir
pedido["cliente"] = "  ana perez "

print("\n" + "=" * 60)
print("LA SOLUCIÓN: **")
print("=" * 60)

# `**pedido` significa "volcá acá adentro todas las claves y valores de pedido".
# Después agregás las que querés cambiar. Las de la DERECHA ganan.
limpio = {**pedido, "cliente": pedido["cliente"].strip().title()}

print("\n  original ->", pedido)
print("  limpio   ->", limpio)
print("\n  ¿son el mismo objeto?", limpio is pedido)
print("  el original quedó intacto:", pedido["cliente"])

print("\n  Se pueden cambiar varias claves a la vez:")
limpio2 = {
    **pedido,
    "cliente": pedido["cliente"].strip().title(),
    "email": pedido["email"].strip().lower(),
}
print("  ->", limpio2)

print("\n" + "=" * 60)
print("CÓMO LEERLO")
print("=" * 60)
print("""
    {**pedido, "cliente": "Ana Perez"}
      ▲         ▲
      │         └── esta clave pisa la que venía de pedido
      └── todas las claves de `pedido`, copiadas

  Es lo mismo que hacer:

      nuevo = dict(pedido)             # copia
      nuevo["cliente"] = "Ana Perez"   # cambio
      return nuevo

  ...pero en una sola expresión, así se puede usar dentro de una comprehension.
""")

print("=" * 60)
print("OJO: la copia es SUPERFICIAL")
print("=" * 60)
anidado = {"nombre": "Ana", "tags": ["vip", "mayorista"]}
copia = {**anidado}
copia["tags"].append("nuevo")
print("  original ->", anidado)
print("  Las claves de primer nivel se copian, pero las listas y dicts de")
print("  adentro se comparten. En el integrador no te afecta (los valores son")
print("  strings y números), pero tenelo presente.")
