from dataclasses import dataclass
@dataclass
class FunctionParameters:
    """Parámetros generales para funciones"""
    amplitude: float = 1.0
    frequency: float = 1.0
    period: float = 2.0
    sampling_rate: float = 1000.0
    duration: float = 4.0
    phase: float = 0.0