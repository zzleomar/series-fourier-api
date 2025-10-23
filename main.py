# API/main.py – FastAPI REST API para Análisis de Fourier
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import numpy as np
import math

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from Analisis_de_Fourier.FourierSynthesizer import FourierSynthesizer
from Funciones_Matematicas.CustomFunction import CustomFunction
from Funciones_Matematicas.PredefinedFunction import PredefinedFunction
from Modelos_de_Datos.FunctionParameters import FunctionParameters

# Crear aplicación FastAPI
app = FastAPI(
    title="Fourier Analysis API",
    description="API REST para análisis y síntesis de Series de Fourier",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS para permitir acceso desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=False,  # Debe ser False cuando allow_origins es ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODELOS DE DATOS (Pydantic)
# ============================================================================

class FunctionRequest(BaseModel):
    """Solicitud para analizar una función"""
    function_type: str = Field(..., description="Tipo de función: Personalizada, Seno, Coseno, etc.")
    expression: Optional[str] = Field(None, description="Expresión matemática para funciones personalizadas")
    amplitude: float = Field(1.0, gt=0, description="Amplitud de la función")
    period: float = Field(2.0, gt=0, description="Período de la función")
    duration: float = Field(10.0, gt=0, le=30, description="Duración de la simulación")
    n_harmonics: int = Field(10, gt=0, le=100, description="Número de armónicos para la Serie de Fourier")
    sampling_rate: int = Field(1000, gt=100, le=10000, description="Frecuencia de muestreo (Hz)")

class FourierCoefficients(BaseModel):
    """Coeficientes de Fourier"""
    a0: float = Field(..., description="Componente DC")
    an: List[float] = Field(..., description="Coeficientes an (coseno)")
    bn: List[float] = Field(..., description="Coeficientes bn (seno)")
    magnitudes: List[float] = Field(..., description="Magnitudes |cn|")
    phases: List[float] = Field(..., description="Fases φn")

class SignalData(BaseModel):
    """Datos de señal"""
    time: List[float] = Field(..., description="Array de tiempo")
    values: List[float] = Field(..., description="Valores de la señal")

class FourierAnalysisResponse(BaseModel):
    """Respuesta completa del análisis de Fourier"""
    metadata: Dict[str, Any] = Field(..., description="Metadatos de la función")
    original_signal: SignalData = Field(..., description="Señal original")
    fourier_approximation: SignalData = Field(..., description="Aproximación de Fourier")
    error_signal: SignalData = Field(..., description="Error de aproximación")
    coefficients: FourierCoefficients = Field(..., description="Coeficientes de Fourier")
    frequency_spectrum: Dict[str, List[float]] = Field(..., description="Espectro de frecuencias (FFT)")
    statistics: Dict[str, float] = Field(..., description="Estadísticas del análisis")

class FunctionInfo(BaseModel):
    """Información de funciones disponibles"""
    name: str
    description: str
    expression_template: str

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Fourier Analysis API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "analyze": "/api/analyze",
            "functions": "/api/functions",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
async def health_check():
    """Verificación de salud del API"""
    return {
        "status": "healthy",
        "service": "Fourier Analysis API",
        "version": "1.0.0"
    }

@app.get("/api/functions", response_model=List[FunctionInfo])
async def get_available_functions():
    """Obtiene lista de funciones predefinidas disponibles"""
    functions = [
        {
            "name": "Seno",
            "description": "Onda sinusoidal pura",
            "expression_template": "A * sin(2*pi*t/T)"
        },
        {
            "name": "Coseno",
            "description": "Onda cosenoidal pura",
            "expression_template": "A * cos(2*pi*t/T)"
        },
        {
            "name": "Onda Cuadrada",
            "description": "Onda cuadrada simétrica",
            "expression_template": "A if sin(2*pi*t/T) >= 0 else -A"
        },
        {
            "name": "Onda Triangular",
            "description": "Onda triangular simétrica",
            "expression_template": "Función triangular predefinida"
        },
        {
            "name": "Onda Diente de Sierra",
            "description": "Onda diente de sierra (rampa)",
            "expression_template": "A * (2*t/T - 1)"
        },
        {
            "name": "Pulso",
            "description": "Tren de pulsos rectangulares",
            "expression_template": "A if t % T < T * 0.1 else 0"
        }
    ]
    return functions

@app.post("/api/analyze", response_model=FourierAnalysisResponse)
async def analyze_function(request: FunctionRequest):
    """
    Analiza una función y retorna:
    - Señal original
    - Aproximación de Fourier
    - Error de aproximación
    - Coeficientes de Fourier
    - Espectro de frecuencias
    - Estadísticas
    """
    try:
        # Crear la función según el tipo
        if request.function_type == "Personalizada":
            if not request.expression:
                raise HTTPException(status_code=400, detail="Se requiere una expresión matemática para funciones personalizadas")

            # Validar que la expresión no esté vacía o solo con espacios
            if not request.expression.strip():
                raise HTTPException(status_code=400, detail="La expresión matemática no puede estar vacía")

            # Validar expresión
            try:
                function = CustomFunction(request.expression, request.amplitude, request.period)

                # Probar evaluación en múltiples puntos para detectar errores
                test_points = [0.0, 0.5, 1.0]
                for t_test in test_points:
                    test_value = function.evaluate(t_test)
                    if not isinstance(test_value, (int, float)) or math.isnan(test_value) or math.isinf(test_value):
                        raise ValueError(f"La expresión produce valores no válidos (NaN o infinito) en t={t_test}")

            except ValueError as e:
                # ValueError ya tiene mensajes descriptivos de CustomFunction
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error al procesar la expresión: {str(e)}")
        else:
            function = PredefinedFunction(request.function_type, request.amplitude, request.period)

        # Configurar sintetizador
        synthesizer = FourierSynthesizer()
        synthesizer.set_function(function)

        # Generar array de tiempo
        dt = 1.0 / request.sampling_rate
        t = np.arange(0, request.duration, dt)

        # Obtener señales
        original_signal = synthesizer.get_original_signal(t)
        fourier_signal = synthesizer.synthesize(t, request.n_harmonics)
        error_signal = original_signal - fourier_signal

        # Calcular coeficientes de Fourier
        coeffs = synthesizer.calculate_coefficients(request.n_harmonics)

        # Calcular magnitudes y fases
        magnitudes = []
        phases = []
        for an, bn in zip(coeffs['an'], coeffs['bn']):
            magnitude = math.sqrt(an**2 + bn**2)
            phase = math.atan2(bn, an) if magnitude > 1e-10 else 0
            magnitudes.append(magnitude)
            phases.append(phase)

        # Calcular FFT
        fft_values = np.fft.fft(original_signal)
        fft_freqs = np.fft.fftfreq(len(original_signal), dt)
        fft_magnitude = np.abs(fft_values)

        # Solo frecuencias positivas hasta 50 Hz
        pos_mask = (fft_freqs > 0) & (fft_freqs <= 50)

        # Estadísticas
        mse = float(np.mean(error_signal**2))
        rmse = float(np.sqrt(mse))
        max_error = float(np.max(np.abs(error_signal)))
        total_energy = float(sum(an**2 + bn**2 for an, bn in zip(coeffs['an'], coeffs['bn'])))

        # Construir respuesta
        response = FourierAnalysisResponse(
            metadata={
                "function_type": request.function_type,
                "expression": request.expression or function.name,
                "amplitude": request.amplitude,
                "period": request.period,
                "duration": request.duration,
                "n_harmonics": request.n_harmonics,
                "sampling_rate": request.sampling_rate,
                "fundamental_frequency": 1.0 / request.period
            },
            original_signal=SignalData(
                time=t.tolist(),
                values=original_signal.tolist()
            ),
            fourier_approximation=SignalData(
                time=t.tolist(),
                values=fourier_signal.tolist()
            ),
            error_signal=SignalData(
                time=t.tolist(),
                values=error_signal.tolist()
            ),
            coefficients=FourierCoefficients(
                a0=coeffs['a0'],
                an=coeffs['an'],
                bn=coeffs['bn'],
                magnitudes=magnitudes,
                phases=phases
            ),
            frequency_spectrum={
                "frequencies": fft_freqs[pos_mask].tolist(),
                "magnitudes": fft_magnitude[pos_mask].tolist()
            },
            statistics={
                "mse": mse,
                "rmse": rmse,
                "max_error": max_error,
                "total_energy": total_energy
            }
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
