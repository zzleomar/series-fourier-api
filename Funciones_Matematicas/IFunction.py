from abc import ABC, abstractmethod
from typing import Dict, Any

class IFunction(ABC):
    """Interfaz para funciones matemáticas"""
    
    @abstractmethod
    def evaluate(self, t: float) -> float:
        """Evalúa la función en el tiempo t"""
        pass
    
    @abstractmethod
    def fourier_coefficients(self, n_harmonics: int) -> Dict[str, Any]:
        """Calcula los coeficientes de Fourier"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre de la función"""
        pass
    
    @property
    @abstractmethod
    def amplitude(self) -> float:
        """Amplitud de la función"""
        pass
    
    @property
    @abstractmethod
    def period(self) -> float:
        """Período de la función"""
        pass
    
    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        """Establece el nombre de la función"""
        pass
    
    @amplitude.setter
    @abstractmethod
    def amplitude(self, value: float) -> None:
        """Establece la amplitud de la función"""
        pass
    
    @period.setter
    @abstractmethod
    def period(self, value: float) -> None:
        """Establece el período de la función"""
        pass