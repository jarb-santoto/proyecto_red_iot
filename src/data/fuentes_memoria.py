"""Adaptadores de fuentes de datos en memoria."""
from src.data.sensores import obtener_registros


def cargar_desde_memoria():
    return obtener_registros()


def preparar_registros_prueba():
    """Escenarios diversos para probar normalización, validación y robustez.

    `obtener_registros()` construye una lista nueva en cada llamada, por lo que
    los 12 registros base nunca se alteran.
    """
    casos = [
        {"id": "  T-PRUEBA-01 ", "tipo": " TEMPERATURA ", "valor": " 21.5 ", "unidad": " °C "},
        {"id": "P-PRUEBA-02", "tipo": "PRESION", "valor": "1012,5", "unidad": "hPa"},
        {"id": "H-PRUEBA-03", "tipo": "humedad", "valor": 55, "unidad": "%"},
        {"id": "", "tipo": "temperatura", "valor": "no-numérico", "unidad": "°C"},
        {"id": "X-PRUEBA-05", "tipo": "radiacion", "valor": 10, "unidad": "W/m2"},
        {"id": "T-PRUEBA-06", "tipo": "temperatura", "valor": 20, "unidad": "hPa"},
        {"id": "T-PRUEBA-07", "tipo": "temperatura", "valor": None, "unidad": "°C"},
    ]
    return obtener_registros() + casos
