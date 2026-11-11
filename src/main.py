"""Punto de entrada de la versión de consola."""
from src.data.fuentes_memoria import cargar_desde_memoria
from src.processing.procesamiento import procesar_registros
from src.interface.consola import mostrar_resumen


def main():
    resultado = procesar_registros(cargar_desde_memoria())
    mostrar_resumen(resultado["resumen"])
    print(f"Inválidos: {len(resultado['registros_invalidos'])} | Errores técnicos: {len(resultado['errores'])}")

if __name__ == "__main__":
    main()
