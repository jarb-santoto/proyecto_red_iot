"""Lectores CSV, JSON y Excel con tolerancia a incidencias por registro.

Los errores estructurales de un registro se convierten en incidencias técnicas
individuales. Los errores que impiden interpretar el archivo completo sí se
propagan como ErrorLecturaFuente/ErrorFormatoFuente.
"""
import csv
import io
import json
from pathlib import Path

from src.exceptions.errores import DataLabError, ErrorLecturaFuente, ErrorFormatoFuente

CAMPOS = ("id", "tipo", "valor", "unidad")


def _leer_texto(archivo):
    try:
        if hasattr(archivo, "read"):
            contenido = archivo.read()
            if hasattr(archivo, "seek"):
                archivo.seek(0)
        else:
            contenido = Path(archivo).read_bytes()
        if isinstance(contenido, bytes):
            return contenido.decode("utf-8-sig")
        return str(contenido)
    except Exception as exc:
        raise ErrorLecturaFuente(f"No fue posible acceder al archivo: {exc}") from exc


def _incidencia_fila(origen, indice, mensaje, identificador=None):
    return {
        "_error_tecnico": str(mensaje),
        "_origen": origen,
        "_fila": indice,
        "id": identificador or f"{origen.lower()}_fila_{indice}",
    }


def _normalizar_filas(filas, origen):
    resultado = []
    for indice, fila in enumerate(filas, start=2):
        if not isinstance(fila, dict):
            resultado.append(_incidencia_fila(
                origen, indice, "La fila no contiene un objeto/diccionario."
            ))
            continue
        if fila.get("_error_tecnico"):
            resultado.append(fila)
            continue
        registro = dict(fila)
        for campo in CAMPOS:
            registro.setdefault(campo, None)
        registro["_origen"] = origen
        registro["_fila"] = indice
        resultado.append(registro)
    return resultado


def leer_csv(archivo):
    try:
        texto = _leer_texto(archivo)
        lector = csv.DictReader(io.StringIO(texto))
        if not lector.fieldnames:
            raise ErrorFormatoFuente("El CSV no contiene encabezados.")
        # Se limpian los encabezados una sola vez; así cada fila ya llega con
        # claves sin espacios ni marca BOM.
        lector.fieldnames = [str(h).strip().lstrip("\ufeff") for h in lector.fieldnames]
        faltantes = set(CAMPOS) - set(lector.fieldnames)
        if faltantes:
            raise ErrorFormatoFuente(
                f"Al CSV le faltan columnas obligatorias: {', '.join(sorted(faltantes))}."
            )

        filas = []
        for numero, fila in enumerate(lector, start=2):
            if None in fila:
                filas.append(_incidencia_fila(
                    "CSV", numero,
                    "La fila contiene más valores que columnas (estructura CSV irregular).",
                    fila.get("id")
                ))
            else:
                filas.append(fila)
        return _normalizar_filas(filas, "CSV")
    except DataLabError:
        raise
    except Exception as exc:
        raise ErrorLecturaFuente(f"No fue posible leer el CSV: {exc}") from exc


def leer_json(archivo):
    try:
        datos = json.loads(_leer_texto(archivo))
        if isinstance(datos, dict):
            if "registros" not in datos:
                raise ErrorFormatoFuente(
                    "El objeto JSON no contiene la clave 'registros'."
                )
            datos = datos["registros"]
        if not isinstance(datos, list):
            raise ErrorFormatoFuente(
                "El JSON debe contener una lista de registros o un objeto con la clave 'registros'."
            )
        return _normalizar_filas(datos, "JSON")
    except DataLabError:
        raise
    except json.JSONDecodeError as exc:
        raise ErrorFormatoFuente(
            f"JSON malformado en línea {exc.lineno}, columna {exc.colno}: {exc.msg}"
        ) from exc
    except Exception as exc:
        raise ErrorLecturaFuente(f"No fue posible leer el JSON: {exc}") from exc


def leer_excel(archivo):
    try:
        import pandas as pd
        if hasattr(archivo, "seek"):
            archivo.seek(0)
        df = pd.read_excel(archivo, dtype=object)
        df.columns = [str(c).strip() for c in df.columns]
        faltantes = set(CAMPOS) - set(df.columns)
        if faltantes:
            raise ErrorFormatoFuente(
                f"Al Excel le faltan columnas obligatorias: {', '.join(sorted(faltantes))}."
            )
        filas = df.where(pd.notna(df), None).to_dict(orient="records")
        return _normalizar_filas(filas, "Excel")
    except DataLabError:
        raise
    except Exception as exc:
        raise ErrorLecturaFuente(f"No fue posible leer el Excel: {exc}") from exc
