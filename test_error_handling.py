#!/usr/bin/env python3
"""
Script de prueba para validar el manejo de errores en expresiones matemáticas
"""
import sys
import os

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from Funciones_Matematicas.CustomFunction import CustomFunction

def test_expression(expression, description):
    """Prueba una expresión y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"Probando: {description}")
    print(f"Expresión: '{expression}'")
    print("-" * 60)

    try:
        func = CustomFunction(expression, amplitude=1.0, period=2.0)
        result = func.evaluate(0.0)
        print(f"✓ Resultado: {result}")
        return True
    except ValueError as e:
        print(f"✗ Error capturado: {e}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {type(e).__name__}: {e}")
        return False

def main():
    print("=" * 60)
    print("PRUEBAS DE MANEJO DE ERRORES EN EXPRESIONES MATEMÁTICAS")
    print("=" * 60)

    # Casos de prueba
    test_cases = [
        # Expresiones válidas
        ("sin(t)", "Función seno válida"),
        ("A * sin(2*pi*t/T)", "Expresión con amplitud y período"),
        ("cos(t) + sin(2*t)", "Suma de funciones trigonométricas"),
        ("exp(-t) * sin(t)", "Exponencial decreciente con seno"),
        ("t**2", "Función cuadrática"),

        # Expresiones inválidas - Sintaxis
        ("sin(t", "Paréntesis sin cerrar"),
        ("sin t)", "Falta paréntesis de apertura"),
        ("sin((t)", "Paréntesis desbalanceados"),
        ("2 * * t", "Operador duplicado"),
        ("", "Expresión vacía"),
        ("   ", "Solo espacios"),

        # Expresiones inválidas - Variables no reconocidas
        ("x + y", "Variables no reconocidas"),
        ("sin(x)", "Variable x no definida"),
        ("myfunction(t)", "Función no reconocida"),

        # Expresiones inválidas - División por cero
        ("1/0", "División directa por cero"),
        ("t/(t-0)", "División por cero cuando t=0"),

        # Expresiones inválidas - Tipo
        ("'hola'", "String en lugar de número"),
        ("None", "Valor None"),

        # Expresiones con problemas matemáticos
        ("sqrt(-1)", "Raíz cuadrada de número negativo"),
        ("log(-1)", "Logaritmo de número negativo"),
        ("log(0)", "Logaritmo de cero"),
    ]

    passed = 0
    failed = 0

    for expression, description in test_cases:
        result = test_expression(expression, description)
        if "válida" in description.lower():
            if result:
                passed += 1
            else:
                failed += 1
        else:
            # Para casos inválidos, esperamos que fallen
            if not result:
                passed += 1
            else:
                failed += 1
                print("⚠️  ADVERTENCIA: Esta expresión inválida no fue detectada!")

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"Total de pruebas: {len(test_cases)}")
    print(f"✓ Exitosas: {passed}")
    print(f"✗ Fallidas: {failed}")
    print("=" * 60)

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
