# API FastAPI - Análisis de Series de Fourier

API REST para el análisis y síntesis de Series de Fourier, extraída de `simulador-fourier-python`.

## Estructura del Proyecto

```
api/
├── main.py                     # Punto de entrada de la API FastAPI
├── requirements.txt            # Dependencias del proyecto
├── run.sh                      # Script de arranque
├── __init__.py
├── Analisis_de_Fourier/       # Módulo de análisis de Fourier
│   ├── FourierAnalysis.py
│   ├── FourierSynthesizer.py
│   ├── IFourierAnalyzer.py
│   └── __init__.py
├── Funciones_Matematicas/     # Módulo de funciones matemáticas
│   ├── CustomFunction.py
│   ├── IFunction.py
│   ├── MathematicalFunction.py
│   ├── PredefinedFunction.py
│   └── __init__.py
└── Modelos_de_Datos/          # Modelos de datos
    ├── FunctionParameters.py
    └── __init__.py
```

## Instalación y Ejecución

### Opción 1: Usando el script de arranque

```bash
cd api
./run.sh
```

### Opción 2: Manual

```bash
cd api

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la API
python main.py
```

## Endpoints Disponibles

### GET /
Información general de la API

### GET /api/health
Verificación de salud del servicio

### GET /api/functions
Lista de funciones predefinidas disponibles:
- Seno
- Coseno
- Onda Cuadrada
- Onda Triangular
- Onda Diente de Sierra
- Pulso

### POST /api/analyze
Analiza una función y retorna el análisis de Fourier completo.

**Request Body:**
```json
{
  "function_type": "Seno",
  "expression": "sin(t)",
  "amplitude": 1.0,
  "period": 2.0,
  "duration": 10.0,
  "n_harmonics": 10,
  "sampling_rate": 1000
}
```

**Response:**
```json
{
  "metadata": {
    "function_type": "Seno",
    "amplitude": 1.0,
    "period": 2.0,
    ...
  },
  "original_signal": {
    "time": [...],
    "values": [...]
  },
  "fourier_approximation": {
    "time": [...],
    "values": [...]
  },
  "error_signal": {
    "time": [...],
    "values": [...]
  },
  "coefficients": {
    "a0": 0.0,
    "an": [...],
    "bn": [...],
    "magnitudes": [...],
    "phases": [...]
  },
  "frequency_spectrum": {
    "frequencies": [...],
    "magnitudes": [...]
  },
  "statistics": {
    "mse": 0.001,
    "rmse": 0.03,
    "max_error": 0.05,
    "total_energy": 1.0
  }
}
```

## Documentación Interactiva

Una vez que la API esté corriendo, puedes acceder a:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos
- **NumPy**: Cálculos numéricos
- **Uvicorn**: Servidor ASGI

## CORS

La API está configurada para aceptar peticiones desde:
- http://localhost:3000
- http://localhost:3001

Para agregar más orígenes, modifica el middleware CORS en `main.py:32-38`
