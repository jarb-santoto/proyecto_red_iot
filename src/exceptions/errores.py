"""Excepciones y normalización de incidencias de DataLab."""
from datetime import datetime, timezone

class DataLabError(Exception):
    """Excepción base de la aplicación."""

class ErrorValidacion(DataLabError):
    """El registro no cumple las reglas de calidad."""

class ErrorFormatoFuente(DataLabError):
    """La estructura de entrada no corresponde al contrato esperado."""

class ErrorLecturaFuente(DataLabError):
    """No fue posible leer una fuente de datos."""


def crear_reporte_error(origen, identificador, mensaje, categoria="PROCESAMIENTO"):
    """Construye una incidencia estructurada sin perder el mensaje original."""
    return {
        "origen": str(origen),
        "identificador": identificador,
        "categoria": str(categoria).upper(),
        "mensaje": str(mensaje),
        "fecha_hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
