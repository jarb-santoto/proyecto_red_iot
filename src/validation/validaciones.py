"""Reglas de calidad de los registros de sensores."""
import math

from src.exceptions.errores import ErrorValidacion

CAMPOS_OBLIGATORIOS = ("id", "tipo", "valor", "unidad")
TIPOS_PERMITIDOS = {"temperatura", "presion", "humedad"}
UNIDADES_POR_TIPO = {"temperatura": {"°C", "C"}, "presion": {"hPa"}, "humedad": {"%"}}

# Límites amplios de plausibilidad para detectar lecturas atípicas evidentes.
# No reemplazan la clasificación pedagógica BAJO/NORMAL/ALTO.
RANGOS_PLAUSIBLES = {
    "temperatura": (-10, 60),
    "humedad": (0, 100),
    "presion": (800, 1100),
}


def esta_vacio(valor):
    """Un campo está vacío si es None o un texto sin contenido."""
    return valor is None or (isinstance(valor, str) and not valor.strip())


def convertir_a_numero(valor):
    """Convierte números y textos numéricos; admite coma decimal sin separador de miles.

    Lanza ErrorValidacion con un mensaje en español si el valor no es numérico.
    """
    if isinstance(valor, bool) or valor is None:
        raise ErrorValidacion("El valor no es numérico.")
    if isinstance(valor, (int, float)):
        numero = float(valor)
    elif isinstance(valor, str):
        texto = valor.strip()
        if not texto:
            raise ErrorValidacion("El valor está vacío.")
        if "," in texto and "." not in texto:
            texto = texto.replace(",", ".")
        try:
            numero = float(texto)
        except ValueError:
            raise ErrorValidacion(f"El valor no es numérico: '{texto}'.") from None
    else:
        raise ErrorValidacion("El valor no tiene un formato numérico admitido.")
    if not math.isfinite(numero):
        raise ErrorValidacion("El valor debe ser un número finito.")
    return numero


def validar_registro(registro):
    """Devuelve (es_valido, motivos), acumulando todos los problemas detectados."""
    if not isinstance(registro, dict):
        return False, ["El registro debe ser un diccionario."]

    motivos = []
    for campo in CAMPOS_OBLIGATORIOS:
        if esta_vacio(registro.get(campo)):
            motivos.append(f"El campo obligatorio '{campo}' está vacío o no existe.")

    # Se normaliza aquí también para que la validación funcione aunque el
    # registro no haya pasado antes por normalizar_registro.
    tipo = registro.get("tipo")
    tipo = tipo.strip().lower() if isinstance(tipo, str) and tipo.strip() else None
    if tipo is not None and tipo not in TIPOS_PERMITIDOS:
        motivos.append(f"Tipo de sensor no permitido: '{tipo}'.")

    unidad = registro.get("unidad")
    if tipo in UNIDADES_POR_TIPO and not esta_vacio(unidad):
        unidad = str(unidad).strip()
        if unidad not in UNIDADES_POR_TIPO[tipo]:
            esperadas = ", ".join(sorted(UNIDADES_POR_TIPO[tipo]))
            motivos.append(f"Unidad '{unidad}' no válida para '{tipo}'. Se esperaba: {esperadas}.")

    valor = registro.get("valor")
    if not esta_vacio(valor):
        try:
            numero = convertir_a_numero(valor)
            if tipo in RANGOS_PLAUSIBLES:
                minimo, maximo = RANGOS_PLAUSIBLES[tipo]
                if not minimo <= numero <= maximo:
                    motivos.append(
                        f"Valor atípico para '{tipo}': {numero}. "
                        f"Rango de plausibilidad del ejercicio: {minimo} a {maximo}."
                    )
        except ErrorValidacion as exc:
            motivos.append(str(exc))

    return len(motivos) == 0, motivos
