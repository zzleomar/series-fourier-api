import numpy as np
import math
from abc import ABC, abstractmethod
from Funciones_Matematicas.IFunction import IFunction

class MathematicalFunction(IFunction, ABC):
    """Clase abstracta para funciones matemáticas"""
    
    def __init__(self, amplitude: float = 1.0, period: float = 2.0):
        self._amplitude = amplitude
        self._period = period
        self._name = "Function"
    
    @abstractmethod
    def evaluate(self, t: float) -> float:
        """Evalúa la función en el tiempo t"""
        pass
    
    def fourier_coefficients(self, n_harmonics: int) -> dict:
        """Calcula los coeficientes de Fourier numéricamente"""
        T = self._period
        omega = 2 * math.pi / T
        
        # Integración numérica para calcular coeficientes
        N_samples = 1000
        dt = T / N_samples
        t_samples = np.linspace(0, T, N_samples, endpoint=False)
        
        # Componente DC (a0)
        f_samples = [self.evaluate(t) for t in t_samples]
        a0 = (2 / T) * np.trapz(f_samples, dx=dt)

        coefficients = {'a0': a0, 'an': [], 'bn': []}

        for n in range(1, n_harmonics + 1):
            # Coeficiente an
            cos_samples = [self.evaluate(t) * math.cos(n * omega * t) for t in t_samples]
            an = (2 / T) * np.trapz(cos_samples, dx=dt)

            # Coeficiente bn
            sin_samples = [self.evaluate(t) * math.sin(n * omega * t) for t in t_samples]
            bn = (2 / T) * np.trapz(sin_samples, dx=dt)
            
            coefficients['an'].append(an)
            coefficients['bn'].append(bn)
        
        return coefficients
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def amplitude(self) -> float:
        return self._amplitude
    
    @property
    def period(self) -> float:
        return self._period
    
    @name.setter
    def name(self, value: str):
        self._name = value
    
    @amplitude.setter
    def amplitude(self, value: float):
        self._amplitude = value
    
    @period.setter
    def period(self, value: float):
        self._period = value