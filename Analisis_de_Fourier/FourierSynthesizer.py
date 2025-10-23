import numpy as np
import math
from Analisis_de_Fourier.IFourierAnalyzer import IFourierAnalyzer
from Funciones_Matematicas.IFunction import IFunction

class FourierSynthesizer(IFourierAnalyzer):
    """Sintetizador de series de Fourier mejorado"""
    
    def __init__(self):
        self._function = None
        self._coefficients = None
    
    def set_function(self, func: IFunction):
        """Establece la función a analizar"""
        self._function = func
        self._coefficients = None
    
    def calculate_coefficients(self, n_harmonics: int) -> dict:
        """Calcula y almacena los coeficientes de Fourier"""
        if self._function is None:
            return {}
        
        self._coefficients = self._function.fourier_coefficients(n_harmonics)
        return self._coefficients
    
    def synthesize(self, t_array: np.ndarray, n_harmonics: int) -> np.ndarray:
        """Sintetiza la señal usando series de Fourier"""
        if self._function is None:
            return np.zeros_like(t_array)
        
        if self._coefficients is None:
            self.calculate_coefficients(n_harmonics)
        
        coeffs = self._coefficients
        T = self._function.period
        omega = 2 * math.pi / T
        
        # Componente DC
        result = np.full_like(t_array, coeffs['a0'] / 2)
        
        # Armónicos
        for n in range(1, min(len(coeffs['an']), n_harmonics) + 1):
            an = coeffs['an'][n-1]
            bn = coeffs['bn'][n-1]
            
            result += an * np.cos(n * omega * t_array) + bn * np.sin(n * omega * t_array)
        
        return result
    
    def get_original_signal(self, t_array: np.ndarray) -> np.ndarray:
        """Obtiene la señal original evaluando la función"""
        if self._function is None:
            return np.zeros_like(t_array)
        
        return np.array([self._function.evaluate(t) for t in t_array])