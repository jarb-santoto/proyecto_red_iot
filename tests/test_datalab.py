import io
import unittest
from src.data.carga_datos import cargar_datos
from src.data.lectores import leer_csv, leer_json
from src.exceptions.errores import ErrorFormatoFuente
from src.data.fuentes_memoria import cargar_desde_memoria, preparar_registros_prueba
from src.processing.procesamiento import procesar_registros
from src.validation.normalizacion import normalizar_registro
from src.validation.validaciones import validar_registro

class DataLabTests(unittest.TestCase):
    def test_normalizacion_no_modifica_original(self):
        original={"id":" A1 ","tipo":" TEMPERATURA ","valor":" 20 ","unidad":" °C "}
        copia=normalizar_registro(original)
        self.assertEqual(copia["tipo"],"temperatura")
        self.assertEqual(original["tipo"]," TEMPERATURA ")

    def test_validacion_acumula_motivos(self):
        ok,motivos=validar_registro({"id":"","tipo":"otro","valor":"x","unidad":""})
        self.assertFalse(ok); self.assertGreaterEqual(len(motivos),3)

    def test_lote_continua_y_separa_resultados(self):
        r=procesar_registros(preparar_registros_prueba())
        self.assertGreater(len(r["registros_validos"]),0)
        self.assertGreater(len(r["registros_invalidos"]),0)
        self.assertEqual(r["resumen"]["total"],len(r["registros_validos"]))

    def test_memoria_base(self):
        r=procesar_registros(cargar_desde_memoria())
        self.assertEqual(len(r["registros_validos"]),12)
        self.assertEqual(len(r["registros_invalidos"]),0)

    def test_promedio_por_sensor(self):
        promedios = procesar_registros(cargar_desde_memoria())["resumen"]["promedio_por_sensor"]
        self.assertAlmostEqual(promedios["temperatura"], (17.5 + 22.0 + 28.4 + 25.0) / 4)
        self.assertAlmostEqual(promedios["presion"], (995.0 + 1010.0 + 1025.0 + 1018.0) / 4)
        self.assertAlmostEqual(promedios["humedad"], (35.0 + 50.0 + 67.0 + 58.0) / 4)


    def test_evento_tecnico_no_detiene_el_lote(self):
        registros = [
            {"id": "T-1", "tipo": "temperatura", "valor": 22, "unidad": "°C"},
            {"id": "T-2", "tipo": "temperatura", "valor": 23, "unidad": "°C",
             "observacion_tecnica": "SIMULACION_TIMEOUT_SENSOR"},
            {"id": "T-3", "tipo": "temperatura", "valor": 24, "unidad": "°C"},
        ]
        resultado = procesar_registros(registros)
        self.assertEqual(len(resultado["registros_validos"]), 2)
        self.assertEqual(len(resultado["errores"]), 1)
        self.assertEqual(resultado["errores"][0]["categoria"], "TIMEOUT_SENSOR")

    def test_error_estructural_individual_no_detiene_lote(self):
        registros = [
            {"id": "P-1", "tipo": "presion", "valor": 1012, "unidad": "hPa"},
            {"id": "P-2", "_error_tecnico": "Fila irregular", "_origen": "CSV", "_fila": 3},
            {"id": "P-3", "tipo": "presion", "valor": 1015, "unidad": "hPa"},
        ]
        resultado = procesar_registros(registros)
        self.assertEqual(len(resultado["registros_validos"]), 2)
        self.assertEqual(len(resultado["errores"]), 1)
        self.assertEqual(resultado["errores"][0]["categoria"], "ESTRUCTURA_REGISTRO")

    def test_motivo_no_numerico_en_espanol(self):
        ok, motivos = validar_registro({"id": "T-1", "tipo": "temperatura", "valor": "abc", "unidad": "°C"})
        self.assertFalse(ok)
        self.assertEqual(motivos, ["El valor no es numérico: 'abc'."])

    def test_unidad_no_textual_es_invalida(self):
        ok, motivos = validar_registro({"id": "H-1", "tipo": "humedad", "valor": 50, "unidad": 5})
        self.assertFalse(ok)
        self.assertIn("Unidad '5' no válida", motivos[0])

    def test_escenarios_de_prueba_no_alteran_base(self):
        registros = preparar_registros_prueba()
        self.assertEqual(registros[:12], cargar_desde_memoria())
        self.assertEqual(len(registros), 19)


class LectoresTests(unittest.TestCase):
    def test_csv_limpia_encabezados_y_conserva_fila(self):
        texto = "﻿ id , tipo ,valor, unidad\nT-1,temperatura,20,°C\n"
        registros = leer_csv(io.BytesIO(texto.encode("utf-8")))
        self.assertEqual(registros[0]["id"], "T-1")
        self.assertEqual(registros[0]["_fila"], 2)
        self.assertEqual(registros[0]["_origen"], "CSV")

    def test_csv_fila_irregular_es_incidencia_individual(self):
        texto = "id,tipo,valor,unidad\nT-1,temperatura,20,°C,extra\nT-2,temperatura,21,°C\n"
        registros = leer_csv(io.StringIO(texto))
        self.assertIn("_error_tecnico", registros[0])
        self.assertEqual(registros[1]["id"], "T-2")

    def test_csv_sin_columnas_obligatorias(self):
        with self.assertRaises(ErrorFormatoFuente):
            leer_csv(io.StringIO("id,tipo\nT-1,temperatura\n"))

    def test_json_malformado(self):
        with self.assertRaises(ErrorFormatoFuente):
            leer_json(io.StringIO("{no es json"))

    def test_json_objeto_sin_clave_registros(self):
        with self.assertRaises(ErrorFormatoFuente):
            leer_json(io.StringIO('{"id": "T-1", "tipo": "temperatura", "valor": 20, "unidad": "°C"}'))

    def test_json_con_clave_registros(self):
        registros = leer_json(io.StringIO('{"registros": [{"id": "P-1", "tipo": "presion", "valor": 1010, "unidad": "hPa"}]}'))
        self.assertEqual(registros[0]["id"], "P-1")

    def test_extension_no_soportada(self):
        with self.assertRaises(ErrorFormatoFuente):
            cargar_datos(io.StringIO(""), "datos.txt")

if __name__ == "__main__": unittest.main()
