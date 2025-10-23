#!/usr/bin/env python3
"""
Script de prueba para validar el manejo de errores en la API
Ejecutar con la API corriendo en http://localhost:8000
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_api_error(expression, description):
    """Prueba una expresión contra la API y muestra el resultado"""
    print(f"\n{'='*70}")
    print(f"Prueba: {description}")
    print(f"Expresión: '{expression}'")
    print("-" * 70)

    payload = {
        "function_type": "Personalizada",
        "expression": expression,
        "amplitude": 1.0,
        "period": 2.0,
        "duration": 10.0,
        "n_harmonics": 10,
        "sampling_rate": 1000
    }

    try:
        response = requests.post(f"{API_URL}/api/analyze", json=payload, timeout=5)

        if response.status_code == 200:
            print("✓ Estado: 200 OK")
            data = response.json()
            print(f"✓ MSE: {data['statistics']['mse']:.6f}")
            return True
        else:
            print(f"✗ Estado: {response.status_code}")
            error_data = response.json()
            print(f"✗ Mensaje de error: {error_data.get('detail', 'Sin detalle')}")
            return False

    except requests.exceptions.ConnectionError:
        print("✗ Error: No se pudo conectar a la API")
        print("   Asegúrate de que la API esté corriendo en http://localhost:8000")
        return None
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return None

def main():
    print("=" * 70)
    print("PRUEBAS DE MANEJO DE ERRORES EN LA API")
    print("=" * 70)
    print(f"API URL: {API_URL}")

    # Verificar que la API está corriendo
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✓ API está corriendo")
        else:
            print("✗ API no responde correctamente")
            return 1
    except:
        print("✗ No se pudo conectar a la API")
        print("   Por favor, ejecuta la API con: python main.py")
        return 1

    # Casos de prueba
    test_cases = [
        # Expresiones válidas
        ("sin(t)", "Función seno válida", True),
        ("A * cos(2*pi*t/T)", "Expresión con amplitud y período", True),

        # Expresiones inválidas
        ("sin(t", "Paréntesis sin cerrar", False),
        ("2 * * t", "Operador duplicado", False),
        ("x + y", "Variables no reconocidas", False),
        ("sin(x)", "Variable x no definida", False),
        ("1/0", "División por cero", False),
        ("sqrt(-1)", "Raíz cuadrada de número negativo", False),
        ("", "Expresión vacía", False),
        ("   ", "Solo espacios", False),
    ]

    passed = 0
    failed = 0
    skipped = 0

    for expression, description, should_succeed in test_cases:
        result = test_api_error(expression, description)

        if result is None:
            skipped += 1
        elif should_succeed == result:
            passed += 1
        else:
            failed += 1
            if should_succeed:
                print("⚠️  ADVERTENCIA: Esta expresión válida fue rechazada!")
            else:
                print("⚠️  ADVERTENCIA: Esta expresión inválida fue aceptada!")

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE PRUEBAS")
    print("=" * 70)
    print(f"Total de pruebas: {len(test_cases)}")
    print(f"✓ Exitosas: {passed}")
    print(f"✗ Fallidas: {failed}")
    print(f"⊘ Omitidas: {skipped}")
    print("=" * 70)

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
