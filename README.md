# aprendiendo-python

Camino de C#/TypeScript → Python intermedio. Ver [ROADMAP.md](ROADMAP.md) para el plan completo.

## Setup (una sola vez)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell se queja con "no se puede cargar el archivo ... Activate.ps1", corré una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Cada vez que te sentás a practicar

```powershell
.\.venv\Scripts\Activate.ps1     # el prompt debe mostrar (.venv)
pytest leccion-01 -v             # correr los tests
ruff format leccion-01           # arreglar espaciado y estilo (PEP 8)
ruff check leccion-01            # detectar imports sin usar, variables muertas, etc.
```

## Cómo va cada lección

| Archivo | Qué es |
|---|---|
| `teoria.md` | Leelo primero. ~15-20 min. |
| `ejercicios_NN.py` | Lo que completás vos. |
| `test_*.py` | Se corrige solo. No lo edites. |
| `solucion_comentada.py` | La versión idiomática. **Abrilo recién cuando tengas todo en verde.** |

Verde en todos los tests **no** significa que el código esté bien escrito.
Cuando pasen, pedime la revisión: ahí es donde se aprende la parte idiomática.

> **¿Por qué `ejercicios_01.py` y no `ejercicios.py`?** Porque Python solo puede tener un
> módulo con un nombre dado cargado a la vez. Con dos archivos `ejercicios.py` en carpetas
> distintas, el segundo test recibía el módulo del primero. El sufijo lo evita sin magia.
> (El tema completo — paquetes, `__init__.py`, imports — está en la Fase 6.)

## Progreso

- [x] Lección 01 — Python para alguien que ya programa *(48/48)*
- [x] Lección 02 — Estructuras de datos y comprehensions *(28/28)*
- [x] Lección 03 — Ordenar, lambdas y `collections` *(27/27)*
- [x] **Integrador Fase 1** — Analizador de ventas *(32/32)* — **Fase 1 completa** 🎉
- [x] Lección 04 — Funciones flexibles, funciones como valores, closures *(46/46)*
- [x] Lección 05 — Decoradores *(36/36)*
- [x] **Integrador Fase 2** — Procesador de tickets de soporte *(36/36)* — **Fase 2 completa** 🎉