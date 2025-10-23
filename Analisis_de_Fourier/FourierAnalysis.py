import numpy as np
import math

# Funciones de utilidad para análisis matemático
class FourierAnalysis:
    """Herramientas adicionales para análisis de Fourier"""
    
    @staticmethod
    def calculate_rms_error(original, approximation):
        """Calcula el error RMS entre señal original y aproximación"""
        return math.sqrt(np.mean((original - approximation)**2))
    
    @staticmethod
    def calculate_thd(coefficients):
        """Calcula la Distorsión Armónica Total"""
        if len(coefficients['an']) < 2:
            return 0
        
        fundamental = math.sqrt(coefficients['an'][0]**2 + coefficients['bn'][0]**2)
        harmonics = sum(coefficients['an'][i]**2 + coefficients['bn'][i]**2 
                       for i in range(1, len(coefficients['an'])))
        
        return math.sqrt(harmonics) / fundamental if fundamental > 0 else 0
    
    @staticmethod
    def find_dominant_frequencies(coefficients, threshold=0.1):
        """Encuentra las frecuencias dominantes en la serie"""
        dominant = []
        max_coeff = max(max(abs(a) for a in coefficients['an']), 
                       max(abs(b) for b in coefficients['bn']))
        
        for n in range(len(coefficients['an'])):
            magnitude = math.sqrt(coefficients['an'][n]**2 + coefficients['bn'][n]**2)
            if magnitude > threshold * max_coeff:
                dominant.append((n+1, magnitude))
        
        return dominant
