from abc import ABC, abstractmethod
from typing import Dict, Any
import numpy as np
from Funciones_Matematicas.IFunction import IFunction

class IFourierAnalyzer(ABC):
    """Interfaz para analizadores de Fourier"""
    
    @abstractmethod
    def set_function(self, func: IFunction) -> None:
        """Establece la función a analizar"""
        pass
    
    @abstractmethod
    def calculate_coefficients(self, n_harmonics: int) -> Dict[str, Any]:
        """Calcula los coeficientes de Fourier"""
        pass
    
    @abstractmethod
    def synthesize(self, t_array: np.ndarray, n_harmonics: int) -> np.ndarray:
        """Sintetiza la señal usando series de Fourier"""
        pass
    
    @abstractmethod
    def get_original_signal(self, t_array: np.ndarray) -> np.ndarray:
        """Obtiene la señal original evaluando la función"""
        pass