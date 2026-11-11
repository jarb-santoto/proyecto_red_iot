"""Orquestación robusta: un registro defectuoso no detiene el lote."""
from src.processing.clasificacion import clasificar_valor
from src.processing.resumen import generar_resumen
from src.validation.normalizacion import normalizar_registro
from src.validation.validaciones import validar_registro, convertir_a_numero
from src.exceptions.errores import crear_reporte_error


EVENTOS_TECNICOS = {
    "SIMULACION_TIMEOUT_SENSOR": (
        "TIMEOUT_SENSOR", "Tiempo de espera agotado al consultar el sensor."
    ),
    "SIMULACION_LECTURA_INTERMITENTE": (
        "LECTURA_INTERMITENTE", "La lectura del sensor fue intermitente."
    ),
    "SIMULACION_PAQUETE_INCOMPLETO": (
        "PAQUETE_INCOMPLETO", "El paquete recibido no contiene todos los datos esperados."
    ),
}


def _registrar_incidencia_tecnica(registro, errores, indice, mensaje, categoria):
    """Agrega a `errores` un reporte con el origen (y la fila, si se conoce)."""
    if not isinstance(registro, dict):
        registro = {}
    origen = registro.get("_origen", "procesamiento")
    if registro.get("_fila") is not None:
        origen = f"{origen}:fila_{registro['_fila']}"
    errores.append(crear_reporte_error(
        origen, registro.get("id") or f"registro_{indice}", mensaje, categoria
    ))


def procesar_registros(registros):
    """Devuelve válidos, inválidos y errores técnicos bajo el contrato DataLab."""
    validos, invalidos, errores = [], [], []
    if registros is None:
        registros = []
    try:
        iterador = iter(registros)
    except TypeError:
        iterador = iter(())
        errores.append(crear_reporte_error(
            "entrada", None, "La fuente debe ser iterable.", "FORMATO_FUENTE"
        ))

    for indice, original in enumerate(iterador, start=1):
        if isinstance(original, dict):
            # Fila que el lector no pudo interpretar (p. ej. CSV irregular).
            if original.get("_error_tecnico"):
                _registrar_incidencia_tecnica(
                    original, errores, indice,
                    original["_error_tecnico"], "ESTRUCTURA_REGISTRO"
                )
                continue
            # Evento técnico simulado: la lectura no es confiable y se excluye
            # del análisis, pero el lote continúa.
            evento = original.get("observacion_tecnica")
            if evento in EVENTOS_TECNICOS:
                categoria, mensaje = EVENTOS_TECNICOS[evento]
                _registrar_incidencia_tecnica(original, errores, indice, mensaje, categoria)
                continue

        try:
            normalizado = normalizar_registro(original)
            es_valido, motivos = validar_registro(normalizado)
            if not es_valido:
                invalidos.append({"registro": normalizado, "motivos": motivos})
                continue
            normalizado["valor"] = convertir_a_numero(normalizado["valor"])
            normalizado["clasificacion"] = clasificar_valor(
                normalizado["valor"], normalizado["tipo"]
            )
            validos.append(normalizado)
        except Exception as exc:
            _registrar_incidencia_tecnica(original, errores, indice, str(exc), "PROCESAMIENTO")

    return {
        "registros_validos": validos,
        "registros_invalidos": invalidos,
        "errores": errores,
        "resumen": generar_resumen(validos),
    }
