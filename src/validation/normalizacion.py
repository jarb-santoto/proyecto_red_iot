"""Normalización y estandarización de registros."""
from copy import deepcopy

CAMPOS_TEXTO = ("id", "tipo", "valor", "unidad")


def normalizar_registro(registro):
    """Devuelve una copia normalizada; nunca modifica el objeto recibido.

    - Quita espacios al inicio y al final de los campos de texto.
    - Escribe el tipo de sensor en minúsculas.
    """
    if not isinstance(registro, dict):
        raise TypeError("El registro debe ser un diccionario.")
    copia = deepcopy(registro)
    for campo in CAMPOS_TEXTO:
        if isinstance(copia.get(campo), str):
            copia[campo] = copia[campo].strip()
    if isinstance(copia.get("tipo"), str):
        copia["tipo"] = copia["tipo"].lower()
    return copia
